"use client";

import { useState } from "react";

interface Props {
  onSubmit: (factPattern: string) => Promise<void>;
  isLoading: boolean;
}

const MIN_CHARS = 50;

export function FactPatternForm({ onSubmit, isLoading }: Props) {
  const [text, setText] = useState("");

  const charCount = text.length;
  const isValid = charCount >= MIN_CHARS;

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!isValid || isLoading) return;
    await onSubmit(text);
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label
          htmlFor="fact-pattern"
          className="block text-sm font-medium text-ink mb-2"
        >
          Opisz stan faktyczny
        </label>
        <div className="relative">
          <textarea
            id="fact-pattern"
            rows={6}
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Opisz sytuację swoimi słowami — relacje między stronami, rodzaj sprawy, potencjalne powiązania..."
            className="w-full border border-border rounded-lg px-4 py-3 text-ink placeholder:text-ink-faint focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent resize-y min-h-[120px]"
            disabled={isLoading}
          />
          <span
            className={`absolute bottom-3 right-3 text-xs ${
              isValid ? "text-ink-faint" : "text-ink-muted"
            }`}
          >
            {charCount}/{MIN_CHARS} min.
          </span>
        </div>
      </div>
      <button
        type="submit"
        disabled={!isValid || isLoading}
        className="w-full px-6 py-3 bg-primary text-white font-medium rounded-lg hover:bg-primary-light transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {isLoading ? "Wysyłanie..." : "Analizuj"}
      </button>
    </form>
  );
}
