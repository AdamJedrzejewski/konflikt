"use client";

import { useEffect, useState } from "react";
import {
  createFeedback,
  getAnalysisFeedback,
  FEEDBACK_KIND_LABELS,
  type Feedback,
  type FeedbackKind,
} from "@/lib/api";

const fieldClass =
  "w-full rounded-lg border border-border bg-white px-3 py-2 text-sm text-ink focus:outline-none focus:ring-2 focus:ring-primary/30";

/** Uwagi do wyniku: lista dotychczasowych i formularz nowej uwagi. */
export function FeedbackPanel({ analysisId }: { analysisId: string }) {
  const [items, setItems] = useState<Feedback[]>([]);
  const [open, setOpen] = useState(false);
  const [kind, setKind] = useState<FeedbackKind>("wynik");
  const [description, setDescription] = useState("");
  const [expected, setExpected] = useState("");
  const [source, setSource] = useState("");
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [saved, setSaved] = useState<string | null>(null);

  useEffect(() => {
    getAnalysisFeedback(analysisId).then(setItems).catch(() => setItems([]));
  }, [analysisId]);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (saving) return;
    setSaving(true);
    setError(null);
    try {
      const item = await createFeedback(analysisId, {
        kind,
        description,
        expected: expected || undefined,
        source: source || undefined,
      });
      setItems((prev) => [item, ...prev]);
      setSaved(item.number);
      setDescription("");
      setExpected("");
      setSource("");
      setOpen(false);
    } catch (err) {
      setError(err instanceof Error ? err.message : String(err));
    } finally {
      setSaving(false);
    }
  }

  return (
    <section className="bg-white rounded-2xl shadow-sm border border-border p-6 space-y-4">
      <div className="flex items-center justify-between gap-4">
        <h2 className="text-base font-semibold">Uwagi do wyniku</h2>
        {!open && (
          <button
            type="button"
            onClick={() => {
              setOpen(true);
              setSaved(null);
            }}
            className="rounded-lg bg-primary px-4 py-2 text-sm font-medium text-white hover:opacity-90"
          >
            Zgłoś uwagę
          </button>
        )}
      </div>

      {saved && <p className="text-sm text-green-700">Zapisano uwagę {saved}.</p>}

      {open && (
        <form onSubmit={handleSubmit} className="space-y-3">
          <label className="block text-sm">
            <span className="font-medium">Rodzaj problemu</span>
            <select className={fieldClass} value={kind} onChange={(e) => setKind(e.target.value as FeedbackKind)}>
              {Object.entries(FEEDBACK_KIND_LABELS).map(([value, label]) => (
                <option key={value} value={value}>
                  {label}
                </option>
              ))}
            </select>
          </label>
          <label className="block text-sm">
            <span className="font-medium">Na czym polega problem</span>
            <textarea
              className={fieldClass}
              rows={4}
              required
              minLength={5}
              value={description}
              onChange={(e) => setDescription(e.target.value)}
            />
          </label>
          <label className="block text-sm">
            <span className="font-medium">Oczekiwane rozstrzygnięcie (opcjonalnie)</span>
            <textarea className={fieldClass} rows={2} value={expected} onChange={(e) => setExpected(e.target.value)} />
          </label>
          <label className="block text-sm">
            <span className="font-medium">Źródło: przepis, orzeczenie, komentarz (opcjonalnie)</span>
            <input className={fieldClass} value={source} onChange={(e) => setSource(e.target.value)} />
          </label>
          <p className="text-xs text-ink-muted">
            Do uwagi zostaną dołączone: ta analiza, wersja aplikacji i wersja bazy wiedzy.
          </p>
          {error && <p className="text-sm text-red-600">{error}</p>}
          <div className="flex gap-3">
            <button
              type="submit"
              disabled={saving}
              className="rounded-lg bg-primary px-4 py-2 text-sm font-medium text-white disabled:opacity-50"
            >
              {saving ? "Zapisywanie..." : "Zapisz uwagę"}
            </button>
            <button type="button" onClick={() => setOpen(false)} className="text-sm text-ink-muted hover:text-ink">
              Anuluj
            </button>
          </div>
        </form>
      )}

      {items.length > 0 && (
        <ul className="space-y-3">
          {items.map((item) => (
            <li key={item.id} className="border-t border-border pt-3 text-sm">
              <p className="font-medium">
                {item.number} · {FEEDBACK_KIND_LABELS[item.kind] ?? item.kind}{" "}
                <span className="text-xs text-ink-muted">({item.status})</span>
              </p>
              <p className="whitespace-pre-wrap">{item.description}</p>
              {item.expected && <p className="text-ink-muted">Oczekiwane: {item.expected}</p>}
              {item.source && <p className="text-ink-muted">Źródło: {item.source}</p>}
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
