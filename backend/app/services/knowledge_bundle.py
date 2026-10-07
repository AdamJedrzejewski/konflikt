"""Read and validate the OBSIL file based knowledge bundle."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any


class KnowledgeBundle:
    """Load accepted research cards without changing their operator status.

    ``project`` is the OBSIL project root (the directory containing
    ``baza_wiedzy``), not the application checkout.
    """

    REGISTRY_PATH = Path("baza_wiedzy/ZREALIZOWANE_OPRACOWANIA.json")
    QUEUE_PATH = Path("baza_wiedzy/kolejka_79/kolejka.json")
    HISTORICAL_MANIFEST_PATH = Path(
        "baza_wiedzy/kandydaci/2026-09-24_proba_3_pojec/00_MANIFEST_ZRODEL.json"
    )

    def __init__(self, project: Path):
        self.project = Path(project).resolve()
        self._file_hashes: dict[str, str] = {}
        self._raw_cards: dict[str, dict[str, Any]] = {}
        self.sources: dict[str, dict[str, Any]] = {}
        self.records: dict[str, dict[str, Any]] = {}
        self.concepts: list[dict[str, Any]] = []
        self.addenda: list[dict[str, Any]] = []
        self._addenda_by_path: dict[str, dict[str, Any]] = {}
        self.record_links: list[dict[str, Any]] = []
        self.question_links: list[dict[str, Any]] = []

        registry_path = self._project_path(self.REGISTRY_PATH)
        queue_path = self._project_path(self.QUEUE_PATH)
        historical_manifest_path = self._project_path(self.HISTORICAL_MANIFEST_PATH)
        self._registry_bytes = self._read_bytes(registry_path)
        self._queue_bytes = self._read_bytes(queue_path)
        self._historical_manifest_bytes = self._read_bytes(historical_manifest_path)
        self.registry = self._json_bytes(self._registry_bytes, registry_path)
        self.queue = self._json_bytes(self._queue_bytes, queue_path)
        historical_manifest = self._json_bytes(
            self._historical_manifest_bytes, historical_manifest_path
        )

        self._validate_registry_shape()
        historical_manifest_hash = self._sha256(self._historical_manifest_bytes)
        declared_historical_hash = self.queue.get("historical_manifest_sha256")
        self._require(
            declared_historical_hash == historical_manifest_hash,
            "Hash historycznego manifestu niezgodny z kolejką",
        )

        self._historical_manifest_key = historical_manifest_hash
        current_manifest_bytes = self._canonical_json(self.queue.get("sources"))
        self._current_manifest_key = self._sha256(current_manifest_bytes)
        self._file_hashes[self._relative(registry_path)] = self._sha256(self._registry_bytes)
        self._file_hashes[self._relative(queue_path)] = self._sha256(self._queue_bytes)
        self._file_hashes[self._relative(historical_manifest_path)] = historical_manifest_hash
        self._file_hashes["@current-source-manifest"] = self._current_manifest_key

        self._load_manifest_sources(historical_manifest, "historical", historical_manifest_hash)
        self._load_manifest_sources(self.queue["sources"], "current", self._current_manifest_key)
        self._load_addenda_and_cards()
        self._validate_bundle_references()
        self.version = self._sha256(self._canonical_json(dict(sorted(self._file_hashes.items()))))

    def metadata(self) -> dict[str, Any]:
        """Return stable counts and the non-approval status of this bundle."""
        return {
            "version": self.version,
            "concepts": len(self.concepts),
            "records": len(self.records),
            "sources": len(self.sources),
            "points": len({point for card in self.concepts for point in card["points"]}),
            "addenda": len(self.addenda),
            "operator_statuses": self._counts(card["operator_status"] for card in self.concepts),
            "completeness": self._counts(card["completeness"] for card in self.concepts),
            "historical_manifest_sha256": self._historical_manifest_key,
            "current_manifest_sha256": self._current_manifest_key,
            "registry_sha256": self._sha256(self._registry_bytes),
        }

    def as_payload(self) -> dict[str, Any]:
        """Return JSON-compatible normalized content for an LLM context builder."""
        payload = {
            "version": self.version,
            "metadata": self.metadata(),
            "sources": self.sources,
            "concepts": [
                {key: value for key, value in concept.items() if not key.startswith("_")}
                for concept in self.concepts
            ],
            "records": self.records,
            "addenda": self.addenda,
            "record_links": self.record_links,
            "question_links": self.question_links,
        }
        # Check at the boundary so callers never discover that provenance contains
        # a non-JSON value after a model call has already been prepared.
        self._canonical_json(payload)
        return payload

    def _load_manifest_sources(self, manifest: Any, origin: str, manifest_hash: str) -> None:
        self._require(isinstance(manifest, list), f"Manifest {origin}: oczekiwano listy")
        seen: set[str] = set()
        for item in manifest:
            self._require(isinstance(item, dict), f"Manifest {origin}: błędny wpis")
            source_id = item.get("id")
            self._require(isinstance(source_id, str) and source_id, f"Manifest {origin}: brak ID")
            self._require(source_id not in seen, f"Powtórzone source ID w manifeście {origin}: {source_id}")
            seen.add(source_id)
            source_key = f"{manifest_hash}::{source_id}"
            source_file = self._project_path(item.get("source"))
            text_file = self._project_path(item.get("text"))
            source_bytes = self._read_bytes(source_file)
            text_bytes = self._read_bytes(text_file)
            expected_source_hash = item.get("source_sha256")
            expected_text_hash = item.get("text_sha256")
            self._require(
                expected_source_hash == self._sha256(source_bytes),
                f"Hash źródła niezgodny: {origin}/{source_id}",
            )
            self._require(
                expected_text_hash == self._sha256(text_bytes),
                f"Hash tekstu źródłowego niezgodny: {origin}/{source_id}",
            )
            normalized_text = text_bytes.decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
            lines = normalized_text.splitlines(keepends=True)
            if item.get("lines") is not None:
                self._require(item["lines"] == len(lines), f"Liczba wierszy niezgodna: {origin}/{source_id}")
            self.sources[source_key] = {
                **item,
                "source_key": source_key,
                "manifest_id": origin,
                "manifest_sha256": manifest_hash,
                "source_path": self._relative(source_file),
                "text_path": self._relative(text_file),
                "line_count": len(lines),
                "actual_characters": len(normalized_text),
            }
            self._file_hashes[self._relative(source_file)] = expected_source_hash
            self._file_hashes[self._relative(text_file)] = expected_text_hash

    def _load_addenda_and_cards(self) -> None:
        registry_entries = self.registry["entries"]
        queue_jobs = self.queue.get("jobs")
        self._require(isinstance(queue_jobs, list), "Kolejka: brak listy jobs")
        jobs: dict[str, dict[str, Any]] = {}
        for job in queue_jobs:
            self._require(isinstance(job, dict) and isinstance(job.get("id"), str), "Kolejka: błędne zadanie")
            self._require(job["id"] not in jobs, f"Powtórzone ID zadania: {job['id']}")
            jobs[job["id"]] = job

        entries_by_id: dict[str, dict[str, Any]] = {}
        for entry in registry_entries:
            entry_id = entry.get("id")
            self._require(isinstance(entry_id, str) and entry_id, "Rejestr: brak ID wpisu")
            self._require(entry_id not in entries_by_id, f"Powtórzone ID wpisu rejestru: {entry_id}")
            entries_by_id[entry_id] = entry

        card_specs: list[tuple[dict[str, Any], str | None, dict[str, Any] | None]] = []
        queue_entry_ids: set[str] = set()
        for job_id, job in jobs.items():
            matched = [
                entry
                for entry in registry_entries
                if entry.get("execution_status") == "ZREALIZOWANE_W_ZAKRESIE_ODBIORU"
                and job_id in entry.get("related_queue_ids", [])
            ]
            self._require(len(matched) == 1, f"Brak jednoznacznego wpisu rejestru dla {job_id}")
            entry = matched[0]
            entry_id = entry["id"]
            queue_entry_ids.add(entry_id)
            artifact = self._project_path(entry.get("path"))
            job_artifact = self._project_path(Path("baza_wiedzy/kolejka_79") / job.get("artifact", ""))
            self._require(artifact == job_artifact, f"Ścieżka karty i kolejki różni się dla {job_id}")
            self._require(
                entry.get("execution_status") == "ZREALIZOWANE_W_ZAKRESIE_ODBIORU",
                f"Nieprawidłowy execution_status: {job_id}",
            )
            self._require(job.get("operator_status") == "OCZEKUJE", f"Status operatora zmieniony: {job_id}")
            self._require(job.get("review_status") in {"CZESCIOWY", "PRZYJETY_KANDYDAT"}, f"Brak odbioru karty: {job_id}")
            card_specs.append((entry, job_id, job))

        historical_entries = [entry for entry in registry_entries if entry.get("execution_status") == "ZREALIZOWANE_W_ZAKRESIE_PROBY"]
        expected_historical = self.queue.get("completed_baseline", {}).get("accepted_partial_cards")
        self._require(
            expected_historical is None or len(historical_entries) == expected_historical,
            "Liczba kart historycznych nie odpowiada completed_baseline",
        )
        for entry in historical_entries:
            card_specs.append((entry, None, None))

        self._require(
            len(card_specs) == len(registry_entries),
            "Rejestr zawiera wpisy spoza historycznej próby i kolejki",
        )

        # Load cards first so cross-card references can be validated as a set.
        for entry, queue_id, job in card_specs:
            card_path = self._project_path(entry.get("path"))
            card_bytes = self._read_bytes(card_path)
            card_hash = self._sha256(card_bytes)
            self._require(entry.get("sha256") == card_hash, f"Hash karty niezgodny: {entry.get('id')}")
            if job is not None:
                self._require(job.get("artifact_sha256") == card_hash, f"Hash karty niezgodny z kolejką: {queue_id}")
                review_artifact = self._project_path(
                    Path("baza_wiedzy/kolejka_79") / job.get("review_artifact", "")
                )
                self._require(
                    review_artifact == self._project_path(entry.get("review_basis")),
                    f"Ścieżka odbioru i kolejki różni się dla {queue_id}",
                )
            card = self._json_bytes(card_bytes, card_path)
            self._require(isinstance(card, dict), f"Karta nie jest obiektem JSON: {entry.get('id')}")
            self._raw_cards[entry["id"]] = card
            self._file_hashes[self._relative(card_path)] = card_hash
            self._add_review_addendum(entry, card, card_hash)
            self._add_explicit_review_addenda(entry, card)
            self.concepts.append(self._normalize_card(entry, card, queue_id, job))

        self._require(len(self.concepts) == len(registry_entries), "Niepełny import kart rejestru")
        for entry in registry_entries:
            self.record_links.extend(entry.get("record_links", []))
        self.record_links.extend(self.registry.get("record_links", []))
        self.question_links.extend(self.registry.get("question_links", []))

    def _add_review_addendum(self, entry: dict[str, Any], card: dict[str, Any], card_hash: str) -> None:
        review_path_value = entry.get("review_basis")
        self._require(isinstance(review_path_value, str) and review_path_value, f"Brak podstawy odbioru: {entry.get('id')}")
        review_path = self._project_path(review_path_value)
        review_bytes = self._read_bytes(review_path)
        content_hash = self._sha256(review_bytes)
        try:
            content = review_bytes.decode("utf-8-sig")
        except UnicodeDecodeError as exc:
            raise ValueError(f"Załącznik odbioru nie jest UTF-8: {review_path_value}") from exc
        addendum: dict[str, Any] = {
            "path": self._relative(review_path),
            "content_sha256": content_hash,
            "content": content,
            "concept_ids": [entry["id"]],
            "operator_status": entry.get("operator_status"),
        }
        if review_path.suffix.lower() == ".json":
            review = self._json_bytes(review_bytes, review_path)
            self._require(isinstance(review, dict), f"Odbiór nie jest obiektem JSON: {review_path_value}")
            if review.get("artifact_sha256") is not None:
                self._require(
                    review["artifact_sha256"] == card_hash,
                    f"Odbiór wskazuje inny hash karty: {entry['id']}",
                )
            if review.get("concept_id") is not None:
                self._require(
                    review["concept_id"] == entry.get("related_queue_ids", [None])[0]
                    or review["concept_id"] == entry.get("id"),
                    f"Odbiór dotyczy innego pojęcia: {entry['id']}",
                )
            addendum["review"] = review
            addendum["integrity"] = "card_hash_verified" if review.get("artifact_sha256") else "content_hash_computed"
        else:
            addendum["integrity"] = "content_hash_computed_no_declared_checksum"
        self._file_hashes[self._relative(review_path)] = content_hash
        existing = self._addenda_by_path.get(addendum["path"])
        if existing is None:
            self._addenda_by_path[addendum["path"]] = addendum
            self.addenda.append(addendum)
        else:
            self._require(existing["content_sha256"] == content_hash, f"Załącznik zmienił się w trakcie odczytu: {review_path_value}")
            existing["concept_ids"].append(entry["id"])

    def _add_explicit_review_addenda(self, entry: dict[str, Any], card: dict[str, Any]) -> None:
        for reference in entry.get("review_addenda", []):
            self._require(isinstance(reference, dict), f"Błędna nota odbioru: {entry['id']}")
            path = self._project_path(reference.get("path"))
            raw = self._read_bytes(path)
            actual_hash = self._sha256(raw)
            self._require(actual_hash == reference.get("sha256"), f"Hash noty odbioru niezgodny: {reference.get('path')}")
            try:
                content = raw.decode("utf-8-sig")
            except UnicodeDecodeError as exc:
                raise ValueError(f"Nota odbioru nie jest UTF-8: {reference.get('path')}") from exc
            basis_record_ids = reference.get("basis_record_ids", [])
            self._require(
                set(basis_record_ids) <= set(entry.get("accepted_record_ids", [])) | set(entry.get("existing_record_refs", [])),
                f"Nota odbioru odwołuje się do nieznanych rekordów: {entry['id']}",
            )
            scope = reference.get("scope")
            card_element_ids = {
                element.get("id")
                for field in ("records", "meanings", "gaps", "questions", "proposals")
                for element in card.get(field, [])
                if isinstance(element, dict)
            }
            self._require(scope in card_element_ids, f"Nota odbioru wskazuje nieznany zakres: {entry['id']}/{scope}")
            addendum = {
                "path": self._relative(path),
                "content_sha256": actual_hash,
                "content": content,
                "concept_ids": [entry["id"]],
                "scope": scope,
                "basis_record_ids": basis_record_ids,
                "precedence": reference.get("precedence"),
                "integrity": "declared_hash_verified",
            }
            self._file_hashes[self._relative(path)] = actual_hash
            previous = self._addenda_by_path.get(addendum["path"])
            if previous is None:
                self._addenda_by_path[addendum["path"]] = addendum
                self.addenda.append(addendum)
            else:
                self._require(previous["content_sha256"] == actual_hash, f"Nota zmieniła się w trakcie odczytu: {reference.get('path')}")
                if entry["id"] not in previous["concept_ids"]:
                    previous["concept_ids"].append(entry["id"])
                previous.setdefault("links", []).append(
                    {key: value for key, value in addendum.items() if key not in {"path", "content", "content_sha256", "concept_ids", "integrity"}}
                )

    def _normalize_card(
        self,
        entry: dict[str, Any],
        card: dict[str, Any],
        queue_id: str | None,
        job: dict[str, Any] | None,
    ) -> dict[str, Any]:
        card_id = entry["id"]
        self._require(entry.get("operator_status") == "OCZEKUJE", f"Status operatora nie jest OCZEKUJE: {card_id}")
        label = entry.get("concept") or card.get("concept") or card.get("label")
        self._require(isinstance(label, str) and label.strip(), f"Brak nazwy pojęcia: {card_id}")
        label = " ".join(label.split())
        manifest_kind = "current" if queue_id else "historical"
        source_manifest_key = self._current_manifest_key if queue_id else self._historical_manifest_key
        expected_records = entry.get("accepted_record_ids")
        self._require(isinstance(expected_records, list), f"Brak accepted_record_ids: {card_id}")
        raw_records = card.get("records", [])
        self._require(isinstance(raw_records, list), f"Nieprawidłowa lista rekordów: {card_id}")
        record_ids = [record.get("id") for record in raw_records]
        self._require(
            record_ids == expected_records,
            f"ID rekordów karty nie odpowiada rejestrowi: {card_id}",
        )
        card_existing_refs = list(card.get("existing_record_refs", []))
        normalized_records = [
            self._normalize_record(record, card_id, source_manifest_key, manifest_kind)
            for record in raw_records
        ]
        for record in normalized_records:
            self._require(record["id"] not in self.records, f"Powtórzone globalne ID rekordu: {record['id']}")
            self.records[record["id"]] = record

        points = list(card.get("points", card.get("scheme_points", [])))
        if job is not None:
            self._require(set(points) == set(job.get("points", [])), f"Punkty karty nie odpowiadają kolejce: {queue_id}")
            points = list(job["points"])
        normalized = {
            "id": card_id,
            "concept_id": queue_id or card.get("concept_id") or entry.get("concept"),
            "label": label,
            "label_normalized": label.casefold(),
            "origin": manifest_kind,
            "execution_status": entry.get("execution_status"),
            "completeness": entry.get("completeness"),
            "source_card_status": card.get("status"),
            "operator_status": entry.get("operator_status"),
            "points": points,
            "accepted_record_ids": list(expected_records),
            "existing_record_refs": card_existing_refs,
            "meanings": card.get("meanings", []),
            "coverage": card.get("coverage", []),
            "relations": card.get("relations", []),
            "gaps": card.get("gaps", []),
            "questions": card.get("questions", []),
            "proposals": card.get("proposals", []),
            "remaining_gap_ids": entry.get("remaining_gap_ids", []),
            "pending_proposal_ids": entry.get("pending_proposal_ids", []),
            "related_queue_ids": entry.get("related_queue_ids", []),
            "reuse_rule": entry.get("reuse_rule"),
            "review": card.get("review"),
            "historical_review": entry.get("historical_review"),
            "source_manifest_sha256": source_manifest_key,
        }
        if queue_id is not None:
            normalized["task_id"] = card.get("task_id")
            normalized["scope"] = card.get("scope")
            normalized["self_check"] = card.get("self_check")
        else:
            normalized["scope"] = card.get("scope")
            normalized["self_check"] = card.get("self_check")
            normalized["control_results"] = card.get("control_results")
        return normalized

    def _normalize_record(
        self, record: dict[str, Any], card_id: str, manifest_hash: str, manifest_kind: str
    ) -> dict[str, Any]:
        self._require(isinstance(record, dict), f"Błędny rekord w {card_id}")
        normalized = dict(record)
        normalized["card_id"] = card_id
        evidence = record.get("evidence", [])
        self._require(isinstance(evidence, list), f"Nieprawidłowe dowody w {record.get('id')}")
        enriched = []
        for item in evidence:
            self._require(isinstance(item, dict), f"Nieprawidłowy dowód w {record.get('id')}")
            source_id = item.get("source_id")
            source_key = f"{manifest_hash}::{source_id}"
            source = self.sources.get(source_key)
            self._require(source is not None, f"Nieznane źródło dla karty {card_id}: {source_id}")
            quote = item.get("quote")
            self._require(isinstance(quote, str) and bool(quote), f"Brak cytatu w {record.get('id')}")
            start, end = item.get("line_start"), item.get("line_end")
            text = self._project_path(source["text_path"]).read_text(encoding="utf-8-sig")
            text = text.replace("\r\n", "\n").replace("\r", "\n")
            lines = text.splitlines(keepends=True)
            self._require(
                type(start) is int and type(end) is int and 1 <= start <= end <= len(lines),
                f"Nieprawidłowy zakres cytatu {record.get('id')} / {source_id}",
            )
            excerpt = "".join(lines[start - 1 : end])
            normalized_quote = quote.replace("\r\n", "\n")
            self._require(
                normalized_quote in excerpt,
                f"Cytat nie odpowiada wierszom źródła: {record.get('id')} / {source_id}",
            )
            if manifest_kind == "current":
                offset = excerpt.find(normalized_quote)
                self._require(
                    offset >= 0
                    and excerpt[:offset].count("\n") == 0
                    and end - start == normalized_quote.count("\n"),
                    f"Zakres wierszy nie wskazuje dokładnego cytatu: {record.get('id')} / {source_id}",
                )
            enriched.append(
                {
                    **item,
                    "source_key": source_key,
                    "source": {
                        key: value
                        for key, value in source.items()
                        if key not in {"source_key"}
                    },
                    "quote": quote,
                    "limits": record.get("limits"),
                    "speaker": record.get("speaker"),
                }
            )
        normalized["evidence"] = enriched
        return normalized

    def _validate_bundle_references(self) -> None:
        global_record_ids = set(self.records)
        self._require(len(global_record_ids) == sum(len(card["accepted_record_ids"]) for card in self.concepts), "Powtórzone ID rekordów")
        concepts_by_id = {card["id"]: card for card in self.concepts}
        self._require(len(concepts_by_id) == len(self.concepts), "Powtórzone ID kart")
        queue_by_id = {job["id"]: job for job in self.queue["jobs"]}

        questions: set[str] = set()
        element_ids_by_card: dict[str, set[str]] = {}
        for concept in self.concepts:
            card_id = concept["id"]
            card = self._raw_cards[card_id]
            current_ids = set(concept["accepted_record_ids"])
            existing_refs = set(concept["existing_record_refs"])
            expected_source_ids = {
                source["id"]
                for source in self.sources.values()
                if source["manifest_sha256"] == concept["source_manifest_sha256"]
            }
            coverage_ids = [item.get("source_id") for item in card.get("coverage", [])]
            self._require(
                len(coverage_ids) == len(set(coverage_ids)) and set(coverage_ids) == expected_source_ids,
                f"Niepełne lub powtórzone pokrycie manifestu w karcie {card_id}",
            )
            self._require(existing_refs <= global_record_ids, f"Nieznane existing_record_refs: {card_id}")
            if concept["origin"] == "historical":
                self._require(not existing_refs, f"Historyczna karta ma zewnętrzne existing_record_refs: {card_id}")
                known_record_refs = current_ids
            else:
                job = queue_by_id[concept["concept_id"]]
                allowed_history: set[str] = set()
                for historical in job.get("historical_cards", []):
                    target = self._load_referenced_card(historical.get("path"), historical.get("sha256"))
                    target_ids = {record.get("id") for record in target.get("records", [])}
                    allowed_history.update(target_ids)
                    basis_ids = set(historical.get("basis_record_ids", []))
                    self._require(
                        basis_ids <= target_ids,
                        f"Nieznany basis_record_id w powiązanej karcie {card_id}",
                    )
                self._require(existing_refs <= allowed_history, f"existing_record_refs bez wskazanej karty historycznej: {card_id}")
                known_record_refs = current_ids | existing_refs

            card_element_ids = set(current_ids)
            for list_name in ("meanings", "gaps", "questions", "proposals"):
                items = card.get(list_name, []) or []
                self._require(isinstance(items, list), f"Nieprawidłowe {list_name}: {card_id}")
                item_ids = [item.get("id") for item in items if isinstance(item, dict)]
                self._require(len(item_ids) == len(items), f"Nieprawidłowy element {list_name}: {card_id}")
                self._require(all(isinstance(item_id, str) and item_id for item_id in item_ids), f"Brak ID w {list_name}: {card_id}")
                self._require(not card_element_ids.intersection(item_ids), f"Powtórzone ID elementów karty: {card_id}")
                card_element_ids.update(item_ids)
                if list_name == "questions":
                    for question_id in item_ids:
                        self._require(question_id not in questions, f"Powtórzone globalne ID pytania: {question_id}")
                        questions.add(question_id)

            for meaning in card.get("meanings", []):
                self._require(
                    set(meaning.get("record_ids", [])) <= known_record_refs,
                    f"Nieznany record_id w znaczeniu {meaning['id']}",
                )
            for question in card.get("questions", []):
                self._require(
                    set(question.get("record_ids", [])) <= known_record_refs,
                    f"Nieznany record_id w pytaniu {question['id']}",
                )
            for gap in card.get("gaps", []):
                basis = set(gap.get("basis_ids", []))
                self._require(basis <= card_element_ids | known_record_refs, f"Nieznana podstawa luki {gap['id']}")
            for record in card.get("records", []):
                self._require(
                    set(record.get("related_record_ids", [])) <= current_ids,
                    f"Nieznany related_record_id w rekordzie {record.get('id')}",
                )
            points = set(concept["points"])
            for relation in card.get("relations", []):
                self._require(isinstance(relation, dict), f"Nieprawidłowa relacja: {card_id}")
                relation_endpoints = {relation.get("from"), relation.get("to")}
                self._require(
                    relation_endpoints <= card_element_ids | points | known_record_refs,
                    f"Nieznany koniec relacji w karcie {card_id}",
                )
                self._require(
                    set(relation.get("record_ids", [])) <= known_record_refs,
                    f"Nieznana podstawa relacji w karcie {card_id}",
                )
            for proposal in card.get("proposals", []):
                self._require(proposal.get("operator_status") == "OCZEKUJE", f"Propozycja nie oczekuje na operatora: {proposal.get('id')}")
                self._require(
                    set(proposal.get("basis_ids", [])) <= card_element_ids | points,
                    f"Nieznana podstawa propozycji: {proposal.get('id')}",
                )
            element_ids_by_card[card_id] = card_element_ids | points | known_record_refs

            for registry_id in concept["remaining_gap_ids"]:
                self._require(registry_id in card_element_ids, f"Nieznane remaining_gap_id: {card_id}/{registry_id}")
            for registry_id in concept["pending_proposal_ids"]:
                self._require(registry_id in card_element_ids, f"Nieznane pending_proposal_id: {card_id}/{registry_id}")

        for link in self.record_links:
            if "from" in link:
                endpoints = {link.get("from"), link.get("to")}
            else:
                endpoints = {link.get("record_id"), *link.get("basis_record_ids", [])}
            self._require(endpoints <= global_record_ids, "Nieznany rekord w record_links")
        for link in self.question_links:
            self._require(link.get("question_id") in questions, "Nieznane question_id w question_links")
            self._require(
                set(link.get("basis_question_ids", [])) <= questions,
                "Nieznany basis_question_id w question_links",
            )

    def _load_referenced_card(self, relative_path: Any, expected_hash: Any) -> dict[str, Any]:
        path = self._project_path(relative_path)
        raw = self._read_bytes(path)
        actual = self._sha256(raw)
        self._require(actual == expected_hash, f"Hash powiązanej karty niezgodny: {relative_path}")
        self._file_hashes[self._relative(path)] = actual
        return self._json_bytes(raw, path)

    def _validate_registry_shape(self) -> None:
        self._require(isinstance(self.registry, dict), "Rejestr nie jest obiektem JSON")
        self._require(isinstance(self.registry.get("entries"), list), "Rejestr nie zawiera entries")
        self._require(isinstance(self.queue, dict), "Kolejka nie jest obiektem JSON")
        self._require(isinstance(self.queue.get("sources"), list), "Kolejka nie zawiera manifestu źródeł")
        self._require(isinstance(self.queue.get("historical_manifest_sha256"), str), "Brak hash historycznego manifestu")

    def _project_path(self, relative: Any) -> Path:
        self._require(isinstance(relative, (str, Path)) and str(relative), "Nieprawidłowa ścieżka w pakiecie")
        # Część plików kolejki zapisano w Windows z separatorem "\\"; na Linuksie byłby częścią nazwy.
        relative = str(relative).replace("\\", "/")
        candidate = (self.project / Path(relative)).resolve()
        self._require(candidate == self.project or self.project in candidate.parents, f"Ścieżka wychodzi poza projekt OBSIL: {relative}")
        return candidate

    def _relative(self, path: Path) -> str:
        return path.resolve().relative_to(self.project).as_posix()

    @staticmethod
    def _read_bytes(path: Path) -> bytes:
        try:
            return path.read_bytes()
        except OSError as exc:
            raise ValueError(f"Nie można odczytać pliku pakietu: {path}") from exc

    @staticmethod
    def _json_bytes(raw: bytes, path: Path) -> Any:
        try:
            return json.loads(raw.decode("utf-8-sig"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError(f"Nieprawidłowy JSON UTF-8: {path}") from exc

    @staticmethod
    def _sha256(raw: bytes) -> str:
        return hashlib.sha256(raw).hexdigest()

    @staticmethod
    def _canonical_json(value: Any) -> bytes:
        try:
            return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
        except (TypeError, ValueError) as exc:
            raise ValueError("Pakiet nie daje się serializować do JSON") from exc

    @staticmethod
    def _counts(values: Any) -> dict[str, int]:
        counts: dict[str, int] = {}
        for value in values:
            key = str(value)
            counts[key] = counts.get(key, 0) + 1
        return counts

    @staticmethod
    def _require(condition: bool, message: str) -> None:
        if not condition:
            raise ValueError(message)
