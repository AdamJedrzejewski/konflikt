"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { getHistory } from "../../lib/api";
import type { Analysis } from "../../types/analysis";
import { AnalysisCard } from "../../components/ui/AnalysisCard";

export default function HistoryPage() {
  const [analyses, setAnalyses] = useState<Analysis[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getHistory()
      .then((data) => {
        setAnalyses(data.items);
      })
      .catch(() => {
        setError("Nie udalo sie pobrac historii analiz.");
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  return (
    <div className="max-w-3xl mx-auto px-6 py-12">
      <h1 className="text-2xl font-bold text-ink mb-8">Historia analiz</h1>

      {/* Loading skeleton */}
      {loading && (
        <div className="space-y-4">
          {[1, 2, 3].map((i) => (
            <div
              key={i}
              className="bg-surface rounded-xl border border-border p-5 animate-pulse"
            >
              <div className="flex items-start gap-4">
                <div className="flex-1 space-y-3">
                  <div className="flex items-center gap-3">
                    <div className="h-5 w-32 bg-surface-subtle rounded-full" />
                    <div className="h-4 w-24 bg-surface-subtle rounded" />
                  </div>
                  <div className="h-4 w-full bg-surface-subtle rounded" />
                </div>
                <div className="h-4 w-20 bg-surface-subtle rounded" />
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Error */}
      {error && (
        <div className="p-4 bg-conflict-obvious/10 border border-conflict-obvious/20 rounded-lg text-sm text-conflict-obvious">
          {error}
        </div>
      )}

      {/* Empty state */}
      {!loading && !error && analyses.length === 0 && (
        <div className="text-center py-16">
          <p className="text-ink-muted mb-6">
            Nie przeprowadzono jeszcze zadnych analiz
          </p>
          <Link
            href="/analyze"
            className="inline-flex items-center px-6 py-3 bg-primary text-white font-medium rounded-lg hover:bg-primary-light transition-colors"
          >
            Pierwsza analiza
          </Link>
        </div>
      )}

      {/* Analysis list */}
      {!loading && !error && analyses.length > 0 && (
        <div className="space-y-3">
          {analyses.map((analysis) => (
            <AnalysisCard key={analysis.id} analysis={analysis} />
          ))}
        </div>
      )}
    </div>
  );
}
