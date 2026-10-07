import type { AnalysisMode } from "../../types/analysis";

interface Props {
  mode: AnalysisMode;
}

const config: Record<
  AnalysisMode,
  { label: string; description: string; colorClass: string }
> = {
  knowledge_test: {
    label: "Test na opracowanej bazie wiedzy",
    description: "Baza częściowa. Decyzje operatora oczekują na rozpatrzenie; wynik wymaga oceny radcy.",
    colorClass: "bg-amber-50 border-amber-200 text-amber-900",
  },
  anchored: {
    label: "Analiza pełna",
    description:
      "Wynik potwierdzony przez bazę reguł i model językowy.",
    colorClass: "bg-emerald-50 border-emerald-200 text-emerald-900",
  },
  llm_only: {
    label: "Analiza wyłącznie LLM",
    description:
      "Baza reguł nie znalazła twardego dopasowania — wynik opiera się wyłącznie na ocenie modelu językowego. Zalecana dodatkowa weryfikacja.",
    colorClass: "bg-amber-50 border-amber-200 text-amber-900",
  },
  error_fallback: {
    label: "Analiza nie powiodła się",
    description:
      "Wystąpił błąd podczas przetwarzania. Spróbuj ponownie lub skontaktuj się z administratorem.",
    colorClass: "bg-red-50 border-red-200 text-red-900",
  },
};

export function AnalysisModeBadge({ mode }: Props) {
  const { label, description, colorClass } = config[mode];
  return (
    <div className={`rounded-2xl border p-4 ${colorClass}`}>
      <p className="text-sm font-semibold">{label}</p>
      <p className="text-xs leading-relaxed mt-1 opacity-90">{description}</p>
    </div>
  );
}
