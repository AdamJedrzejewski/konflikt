"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { getAnalysis } from "@/lib/api";
import type { Analysis } from "@/types/analysis";
import { ConflictBadge } from "@/components/ui/ConflictBadge";
import { RiskCard } from "@/components/ui/RiskCard";
import { LegalBasis } from "@/components/ui/LegalBasis";
import { LoadingSpinner } from "@/components/ui/LoadingSpinner";
import { AnalysisModeBadge } from "@/components/ui/AnalysisModeBadge";
import { FeedbackPanel } from "@/components/ui/FeedbackPanel";

const CLASSIFICATION_LABELS: Record<string, string> = {
  brak_konfliktu: "Brak konfliktu interesów",
  potencjalny_konflikt: "Potencjalny konflikt interesów",
  wysoki_poziom_ryzyka: "Wysoki poziom ryzyka konfliktu",
  konflikt_oczywisty: "Konflikt interesów (przypadek oczywisty)",
  // Backend (KERP pipeline) returns enum-like uppercase strings — map to UI labels
  NO_CONFLICT: "Brak stwierdzonego konfliktu w zbadanym zakresie",
  CONFLICT_WAIVABLE: "Konflikt uchylalny (za zgodą klientów)",
  CONFLICT: "Konflikt interesów",
  UNKNOWN: "Nie udało się ustalić",
  UNCLEAR: "Brak podstaw do rozstrzygnięcia w dostępnym zakresie",
};

// Map backend classification → ConflictBadge classification key
const BADGE_KEY_MAP: Record<string, string> = {
  NO_CONFLICT: "brak_konfliktu",
  CONFLICT_WAIVABLE: "potencjalny_konflikt",
  CONFLICT: "konflikt_oczywisty",
};

export default function ResultPage() {
  const { id } = useParams<{ id: string }>();
  const router = useRouter();
  const [analysis, setAnalysis] = useState<Analysis | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getAnalysis(id).then((data) => {
      setAnalysis(data);
      setLoading(false);
      if (data.status !== "complete" && data.status !== "error") {
        setTimeout(() => router.refresh(), 2000);
      }
    });
  }, [id, router]);

  if (loading) return <div className="flex justify-center py-20"><LoadingSpinner text="Ładowanie wyniku..." /></div>;
  if (!analysis) return <p className="text-center py-20 text-ink-muted">Analiza nie znaleziona.</p>;
  if (analysis.status === "error") {
    return (
      <main className="max-w-3xl mx-auto px-4 py-10 space-y-6">
        <p className="text-center text-red-600">Błąd podczas analizy. Spróbuj ponownie.</p>
        <FeedbackPanel analysisId={analysis.id} />
      </main>
    );
  }
  if (analysis.status !== "complete") return <div className="flex justify-center py-20"><LoadingSpinner text="Analiza w toku..." /></div>;

  const r = analysis.final_result;
  const mode = r?.mode;
  const classification = analysis.conflict_classification;
  const badgeKey = classification
    ? (BADGE_KEY_MAP[classification] ?? classification)
    : null;
  const classLabel = classification
    ? (CLASSIFICATION_LABELS[classification] ?? "Nieznana klasyfikacja")
    : "Nieznana klasyfikacja";

  if (mode === "error_fallback") {
    return (
      <main className="max-w-3xl mx-auto px-4 py-10 space-y-6">
        <AnalysisModeBadge mode="error_fallback" />
        {r?.justification && (
          <div className="bg-white rounded-2xl shadow-sm border border-border p-6">
            <p className="text-sm text-ink leading-relaxed whitespace-pre-wrap">
              {r.justification}
            </p>
          </div>
        )}
        <FeedbackPanel analysisId={analysis.id} />
        <div className="text-center">
          <button
            onClick={() => router.push("/analyze")}
            className="text-sm text-primary hover:underline"
          >
            ← Spróbuj ponownie
          </button>
        </div>
      </main>
    );
  }

  return (
    <main className="max-w-3xl mx-auto px-4 py-10 space-y-8">

      {/* Tryb analizy */}
      {mode && <AnalysisModeBadge mode={mode} />}

      {r?.knowledge && (
        <div className="text-sm text-ink-muted space-y-1">
          <p>Model: {r.model_connection?.model ?? "nie podano"}. Baza: {r.knowledge.concepts} opracowania, {r.knowledge.records} rekordów.</p>
          <p>Wersja wiedzy: <code>{r.knowledge.version.slice(0, 12)}</code>. Status operatora: {r.knowledge.operator_status}.</p>
        </div>
      )}

      {/* Klasyfikacja */}
      <div className="bg-white rounded-2xl shadow-sm border border-border p-8 text-center space-y-3">
        <p className="text-xs font-semibold text-ink-muted uppercase tracking-widest">Wynik analizy</p>
        {badgeKey && (
          <ConflictBadge
            classification={badgeKey as Parameters<typeof ConflictBadge>[0]["classification"]}
            size="lg"
          />
        )}
        <h1 className="text-2xl font-bold text-ink">{classLabel}</h1>
        <div className="flex justify-center gap-3 flex-wrap">
          {analysis.risk_level && (
            <span className="text-sm bg-surface-muted border border-border rounded-full px-3 py-1 text-ink-muted">
              Ryzyko: <strong>{analysis.risk_level}</strong>
            </span>
          )}
          {analysis.confidence_level && (
            <span className="text-sm bg-surface-muted border border-border rounded-full px-3 py-1 text-ink-muted">
              Pewność: <strong>{analysis.confidence_level}</strong>
            </span>
          )}
        </div>
      </div>

      {/* Stan faktyczny — zwinięty */}
      {analysis.fact_pattern && (
        <details className="bg-white rounded-2xl shadow-sm border border-border">
          <summary className="px-6 py-4 cursor-pointer text-sm font-semibold text-ink hover:bg-surface-subtle transition-colors rounded-2xl">
            Opis stanu faktycznego
          </summary>
          <div className="px-6 pb-6 pt-2">
            <p className="text-sm text-ink-muted whitespace-pre-wrap leading-relaxed">
              {analysis.fact_pattern}
            </p>
          </div>
        </details>
      )}

      {/* Uzasadnienie */}
      {r?.justification && (
        <div className="bg-white rounded-2xl shadow-sm border border-border p-6 space-y-3">
          <h2 className="text-base font-semibold text-ink">Uzasadnienie</h2>
          <p className="text-sm text-ink leading-relaxed whitespace-pre-wrap">{r.justification}</p>
          <LegalBasis articles={r.legal_basis ?? []} />
        </div>
      )}

      {/* Analiza ryzyka */}
      {r && (r.confidential_information_risk || r.adversity_risk || r.successive_representation_risk || r.organizational_barriers) && (
        <div className="space-y-3">
          <h2 className="text-base font-semibold text-ink px-1">Szczegółowa analiza ryzyka</h2>
          <div className="grid grid-cols-2 gap-3">
            <RiskCard title="Tajemnica zawodowa" value={r.confidential_information_risk} />
            <RiskCard title="Sprzeczność interesów" value={r.adversity_risk} />
            <RiskCard title="Uprzednia reprezentacja" value={r.successive_representation_risk} />
            <RiskCard title="Bariery organizacyjne" value={r.organizational_barriers} />
          </div>
        </div>
      )}

      {/* Braki informacyjne */}
      {r?.missing_information && r.missing_information.length > 0 && (
        <div className="bg-amber-50 border border-amber-200 rounded-2xl p-6 space-y-2">
          <h2 className="text-sm font-semibold text-amber-800">&#9888;&#65039; Braki informacyjne</h2>
          <ul className="space-y-1">
            {r.missing_information.map((item, i) => (
              <li key={i} className="text-sm text-amber-900">• {item}</li>
            ))}
          </ul>
        </div>
      )}

      {r?.knowledge_gaps && r.knowledge_gaps.length > 0 && (
        <div className="bg-amber-50 border border-amber-200 rounded-2xl p-6 space-y-2">
          <h2 className="text-sm font-semibold text-amber-800">Luki w wiedzy</h2>
          <ul className="list-disc pl-5 text-sm text-amber-900">{r.knowledge_gaps.map((text, i) => <li key={i}>{text}</li>)}</ul>
        </div>
      )}
      {r?.unassessed_scope && r.unassessed_scope.length > 0 && (
        <div className="bg-white border border-border rounded-2xl p-6 space-y-2">
          <h2 className="text-sm font-semibold">Zakres nieoceniony</h2>
          <ul className="list-disc pl-5 text-sm">{r.unassessed_scope.map((text, i) => <li key={i}>{text}</li>)}</ul>
        </div>
      )}
      {r?.sources_used && r.sources_used.length > 0 && (
        <section className="space-y-3">
          <h2 className="text-base font-semibold">Podstawy odczytane z bazy</h2>
          {r.sources_used.map((record) => (
            <details key={record.id} className="bg-white border border-border rounded-2xl p-5">
              <summary className="cursor-pointer text-sm font-semibold">{record.id}: {record.claim}</summary>
              <div className="mt-3 space-y-3 text-sm">
                {record.speaker && <p>Autor stanowiska: {record.speaker}</p>}
                {record.limits && <p>Ograniczenia: {record.limits}</p>}
                {record.evidence.map((evidence, index) => (
                  <div key={index} className="space-y-2">
                    <blockquote className="border-l-2 border-border pl-3 whitespace-pre-wrap">{evidence.quote}</blockquote>
                    <p className="text-xs text-ink-muted break-words">{evidence.source?.text_path ?? evidence.source_id}, wiersze {evidence.line_start}–{evidence.line_end}.</p>
                  </div>
                ))}
              </div>
            </details>
          ))}
        </section>
      )}

      <FeedbackPanel analysisId={analysis.id} />

      {/* Disclaimer */}
      <div className="bg-surface-muted border border-border rounded-2xl p-6">
        <p className="text-xs text-ink-muted leading-relaxed">
          Narzędzie OBSIL ma charakter wspomagający. Powyższa analiza nie stanowi porady prawnej
          ani wiążącej oceny prawnej. Finalna ocena istnienia konfliktu interesów należy do radcy prawnego.
        </p>
      </div>

      <div className="text-center">
        <button
          onClick={() => router.push("/analyze")}
          className="text-sm text-primary hover:underline"
        >
          ← Nowa analiza
        </button>
      </div>

    </main>
  );
}
