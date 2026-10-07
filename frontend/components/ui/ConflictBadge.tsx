import { cn } from "@/lib/utils";
import type { ConflictClassification } from "../../types/analysis";

interface Props {
  classification: ConflictClassification;
  size?: "sm" | "lg";
}

const config: Record<
  ConflictClassification,
  { label: string; icon: string; colorClass: string }
> = {
  UNCLEAR: { label: "Brak rozstrzygnięcia", icon: "?", colorClass: "bg-amber-50 text-amber-900 border-amber-200" },
  UNKNOWN: { label: "Nie ustalono wyniku", icon: "?", colorClass: "bg-amber-50 text-amber-900 border-amber-200" },
  brak_konfliktu: {
    label: "Brak konfliktu",
    icon: "\u2713",
    colorClass: "bg-conflict-none/10 text-conflict-none border-conflict-none/30",
  },
  potencjalny_konflikt: {
    label: "Potencjalny konflikt",
    icon: "!",
    colorClass:
      "bg-conflict-potential/10 text-conflict-potential border-conflict-potential/30",
  },
  wysoki_poziom_ryzyka: {
    label: "Wysoki poziom ryzyka",
    icon: "!!",
    colorClass:
      "bg-conflict-high/10 text-conflict-high border-conflict-high/30",
  },
  konflikt_oczywisty: {
    label: "Konflikt oczywisty",
    icon: "\u2717",
    colorClass:
      "bg-conflict-obvious/10 text-conflict-obvious border-conflict-obvious/30",
  },
};

export function ConflictBadge({ classification, size = "sm" }: Props) {
  const { label, icon, colorClass } = config[classification] ?? config.UNKNOWN;

  return (
    <span
      className={cn(
        "inline-flex items-center gap-1.5 rounded-full border font-semibold",
        colorClass,
        size === "lg" ? "px-4 py-2 text-base" : "px-2.5 py-0.5 text-xs"
      )}
    >
      <span className="font-bold">{icon}</span>
      {label}
    </span>
  );
}
