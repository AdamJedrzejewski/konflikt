"use client";

import { useState } from "react";
import type { ClarificationQuestion } from "../../types/analysis";

interface Props {
  questions: ClarificationQuestion[];
  onSubmit: (answers: { question_id: string; answer: string }[]) => Promise<void>;
  isLoading: boolean;
}

export function ClarificationForm({ questions, onSubmit, isLoading }: Props) {
  const [answers, setAnswers] = useState<string[]>(
    () => new Array(questions.length).fill("")
  );

  function updateAnswer(index: number, value: string) {
    setAnswers((prev) => {
      const next = [...prev];
      next[index] = value;
      return next;
    });
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (isLoading) return;

    const payload = questions.map((q, i) => ({
      question_id: q.id,
      answer: answers[i],
    }));

    await onSubmit(payload);
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div>
        <h2 className="text-lg font-semibold text-ink mb-1">
          Pytania uzupełniające
        </h2>
        <p className="text-sm text-ink-muted mb-6">
          Odpowiedzi są opcjonalne — możesz pominąć pytania, na które nie znasz
          odpowiedzi.
        </p>
      </div>

      <div className="space-y-5">
        {questions.map((q, i) => (
          <div key={q.id}>
            <label
              htmlFor={`q-${i}`}
              className="block text-sm font-medium text-ink mb-1.5"
            >
              {i + 1}. {q.question}
            </label>
            <input
              id={`q-${i}`}
              type="text"
              value={answers[i]}
              onChange={(e) => updateAnswer(i, e.target.value)}
              placeholder="Twoja odpowiedź (opcjonalna)"
              className="w-full border border-border rounded-lg px-4 py-2.5 text-ink placeholder:text-ink-faint focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
              disabled={isLoading}
            />
          </div>
        ))}
      </div>

      <button
        type="submit"
        disabled={isLoading}
        className="w-full px-6 py-3 bg-primary text-white font-medium rounded-lg hover:bg-primary-light transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {isLoading ? "Wysyłanie..." : "Prześlij odpowiedzi"}
      </button>
    </form>
  );
}
