interface LegalBasisProps {
  articles: string[];
}

export function LegalBasis({ articles }: LegalBasisProps) {
  if (!articles?.length) return null;
  return (
    <div className="mt-3">
      <p className="text-xs font-semibold text-ink-muted uppercase tracking-wide mb-2">Podstawa prawna</p>
      <div className="flex flex-wrap gap-2">
        {articles.map((a) => (
          <span key={a} className="text-xs bg-primary/10 text-primary font-medium px-2 py-1 rounded-md">
            {a}
          </span>
        ))}
      </div>
    </div>
  );
}
