"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import {
  getFeedback,
  getMe,
  FEEDBACK_EXPORT_URL,
  FEEDBACK_KIND_LABELS,
  type Feedback,
  type Me,
} from "@/lib/api";
import { LoadingSpinner } from "@/components/ui/LoadingSpinner";

export default function FeedbackRegisterPage() {
  const [items, setItems] = useState<Feedback[] | null>(null);
  const [me, setMe] = useState<Me | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getFeedback()
      .then(setItems)
      .catch((err) => setError(err instanceof Error ? err.message : String(err)));
    getMe().then(setMe).catch(() => setMe(null));
  }, []);

  const isOperator = me?.role === "operator";

  return (
    <main className="max-w-5xl mx-auto px-4 py-10 space-y-6">
      <div className="flex items-center justify-between gap-4">
        <h1 className="text-2xl font-bold">{isOperator ? "Rejestr uwag" : "Moje uwagi"}</h1>
        {isOperator && (
          <a href={FEEDBACK_EXPORT_URL} className="text-sm text-primary hover:underline">
            Pobierz CSV
          </a>
        )}
      </div>

      {error && <p className="text-red-600">{error}</p>}
      {!items && !error && <LoadingSpinner text="Ładowanie uwag..." />}
      {items && items.length === 0 && (
        <p className="text-ink-muted">Brak uwag. Uwagę zgłasza się przyciskiem „Zgłoś uwagę” pod wynikiem analizy.</p>
      )}

      {items && items.length > 0 && (
        <div className="overflow-x-auto">
          <table className="w-full text-sm border-collapse">
            <thead>
              <tr className="text-left border-b border-border">
                <th className="py-2 pr-3">Numer</th>
                <th className="py-2 pr-3">Data</th>
                {isOperator && <th className="py-2 pr-3">Autor</th>}
                <th className="py-2 pr-3">Rodzaj</th>
                <th className="py-2 pr-3">Opis</th>
                <th className="py-2 pr-3">Status</th>
                <th className="py-2">Analiza</th>
              </tr>
            </thead>
            <tbody>
              {items.map((item) => (
                <tr key={item.id} className="border-b border-border align-top">
                  <td className="py-2 pr-3 font-medium">{item.number}</td>
                  <td className="py-2 pr-3 whitespace-nowrap">{new Date(item.created_at).toLocaleString("pl-PL")}</td>
                  {isOperator && <td className="py-2 pr-3">{item.author_email}</td>}
                  <td className="py-2 pr-3">{FEEDBACK_KIND_LABELS[item.kind] ?? item.kind}</td>
                  <td className="py-2 pr-3 whitespace-pre-wrap">{item.description}</td>
                  <td className="py-2 pr-3">{item.status}</td>
                  <td className="py-2">
                    <Link href={`/analyze/${item.analysis_id}/result`} className="text-primary hover:underline">
                      Otwórz
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </main>
  );
}
