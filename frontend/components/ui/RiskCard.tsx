interface RiskCardProps {
  title: string;
  value: string;
  description?: string;
}

const riskColors: Record<string, string> = {
  brak: "bg-green-50 border-green-200 text-green-800",
  niskie: "bg-green-50 border-green-200 text-green-700",
  srednie: "bg-amber-50 border-amber-200 text-amber-800",
  wysokie: "bg-orange-50 border-orange-200 text-orange-800",
  krytyczne: "bg-red-50 border-red-200 text-red-800",
  czesciowe: "bg-amber-50 border-amber-200 text-amber-800",
  pelne: "bg-green-50 border-green-200 text-green-800",
};

export function RiskCard({ title, value, description }: RiskCardProps) {
  const colorClass = riskColors[value] ?? "bg-gray-50 border-gray-200 text-gray-700";
  return (
    <div className={`rounded-xl border p-4 ${colorClass}`}>
      <p className="text-xs font-semibold uppercase tracking-wide opacity-70 mb-1">{title}</p>
      <p className="text-sm font-bold capitalize">{value}</p>
      {description && <p className="text-xs mt-1 opacity-80">{description}</p>}
    </div>
  );
}
