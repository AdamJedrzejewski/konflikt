"use client";

interface Props {
  text?: string;
}

export function LoadingSpinner({ text }: Props) {
  return (
    <div className="flex flex-col items-center gap-4">
      <div className="w-10 h-10 border-3 border-primary/20 border-t-primary rounded-full animate-spin" />
      {text && <p className="text-sm text-ink-muted">{text}</p>}
    </div>
  );
}
