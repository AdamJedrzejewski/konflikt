import Link from "next/link";
import type { Analysis } from "../../types/analysis";
import { ConflictBadge } from "./ConflictBadge";

interface Props {
  analysis: Analysis;
}

function formatDate(iso: string): string {
  const date = new Date(iso);
  return date.toLocaleDateString("pl-PL", {
    day: "numeric",
    month: "long",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

function truncate(text: string, maxLength: number): string {
  if (text.length <= maxLength) return text;
  return text.slice(0, maxLength) + "...";
}

export function AnalysisCard({ analysis }: Props) {
  return (
    <div className="bg-surface rounded-xl border border-border p-5 hover:shadow-sm transition-shadow">
      <div className="flex items-start justify-between gap-4">
        <div className="flex-1 min-w-0 space-y-2">
          <div className="flex items-center gap-3">
            {analysis.conflict_classification && (
              <ConflictBadge
                classification={analysis.conflict_classification}
                size="sm"
              />
            )}
            <span className="text-xs text-ink-muted">
              {formatDate(analysis.created_at)}
            </span>
          </div>
          {analysis.fact_pattern && (
            <p className="text-sm text-ink-muted leading-relaxed">
              {truncate(analysis.fact_pattern, 100)}
            </p>
          )}
        </div>
        <Link
          href={`/analyze/${analysis.id}/result`}
          className="text-sm text-primary hover:underline whitespace-nowrap font-medium"
        >
          Szczegoly →
        </Link>
      </div>
    </div>
  );
}
