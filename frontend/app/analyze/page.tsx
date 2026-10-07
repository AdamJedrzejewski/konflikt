"use client";

import { useState, useCallback, useRef } from "react";
import { useRouter } from "next/navigation";
import { createAnalysis, getAnalysis, submitClarification } from "../../lib/api";
import type { Analysis } from "../../types/analysis";
import { FactPatternForm } from "../../components/ui/FactPatternForm";
import { ClarificationForm } from "../../components/ui/ClarificationForm";
import { LoadingSpinner } from "../../components/ui/LoadingSpinner";

type PageState = "form" | "loading" | "clarification" | "error";

const POLL_TIMEOUT_MS = 240_000;

export default function AnalyzePage() {
  const router = useRouter();
  const [pageState, setPageState] = useState<PageState>("form");
  const [analysis, setAnalysis] = useState<Analysis | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const pollStartRef = useRef<number | null>(null);

  const pollAnalysis = useCallback(
    async (id: string) => {
      if (pollStartRef.current === null) {
        pollStartRef.current = Date.now();
      }
      try {
        const data = await getAnalysis(id);
        setAnalysis(data);

        // Pending with clarifying questions — show clarification form
        if (data.status === "pending" && data.clarifying_questions?.length) {
          pollStartRef.current = null;
          setPageState("clarification");
          return;
        }

        if (data.status === "complete") {
          pollStartRef.current = null;
          if (data.clarifying_questions?.length) {
            setPageState("clarification");
          } else {
            router.push(`/analyze/${data.id}/result`);
          }
          return;
        }

        if (data.status === "error") {
          pollStartRef.current = null;
          setError("Wystąpił błąd podczas analizy. Spróbuj ponownie.");
          setPageState("error");
          return;
        }

        // Polling timeout — przerwij i pokaż komunikat zamiast wisieć
        if (Date.now() - pollStartRef.current > POLL_TIMEOUT_MS) {
          pollStartRef.current = null;
          setError(
            "Analiza trwa wyjątkowo długo (>4 min). Sprawdź historię za chwilę lub spróbuj ponownie."
          );
          setPageState("error");
          return;
        }

        // Still processing — poll again
        setTimeout(() => pollAnalysis(id), 2000);
      } catch {
        pollStartRef.current = null;
        setError("Nie udało się pobrać statusu analizy.");
        setPageState("error");
      }
    },
    [router]
  );

  async function handleSubmitFactPattern(factPattern: string) {
    setIsSubmitting(true);
    setError(null);
    try {
      const data = await createAnalysis(factPattern);
      setAnalysis(data);
      setPageState("loading");
      setTimeout(() => pollAnalysis(data.id), 2000);
    } catch (err) {
      const msg = err instanceof Error ? err.message : String(err);
      setError(`Błąd: ${msg}`);
      setPageState("error");
    } finally {
      setIsSubmitting(false);
    }
  }

  async function handleSubmitClarification(
    answers: { question_id: string; answer: string }[]
  ) {
    if (!analysis) return;
    setIsSubmitting(true);
    setError(null);
    try {
      await submitClarification(analysis.id, answers);
      setPageState("loading");
      setTimeout(() => pollAnalysis(analysis.id), 2000);
    } catch (err) {
      const msg = err instanceof Error ? err.message : String(err);
      setError(`Błąd: ${msg}`);
      setPageState("error");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <div className="max-w-2xl mx-auto px-6 py-12">
      <div className="bg-surface rounded-xl shadow-sm border border-border p-8">
        {/* Form state */}
        {(pageState === "form" || pageState === "error") && (
          <>
            <h1 className="text-2xl font-bold text-ink mb-2">Nowa analiza</h1>
            <p className="text-sm text-ink-muted mb-8">
              Opisz sytuację, a system pomoże ocenić ryzyko konfliktu interesów.
            </p>
            {error && (
              <div className="mb-6 p-4 bg-conflict-obvious/10 border border-conflict-obvious/20 rounded-lg text-sm text-conflict-obvious">
                {error}
              </div>
            )}
            <FactPatternForm
              onSubmit={handleSubmitFactPattern}
              isLoading={isSubmitting}
            />
          </>
        )}

        {/* Loading state */}
        {pageState === "loading" && (
          <div className="py-16">
            <LoadingSpinner text="Analizuję stan faktyczny..." />
            <div className="mt-8 mx-auto max-w-xs">
              <div className="h-1.5 bg-surface-subtle rounded-full overflow-hidden">
                <div className="h-full bg-primary rounded-full animate-pulse w-2/3" />
              </div>
            </div>
          </div>
        )}

        {/* Clarification state */}
        {pageState === "clarification" &&
          analysis?.clarifying_questions &&
          analysis.clarifying_questions.length > 0 && (
            <ClarificationForm
              questions={analysis.clarifying_questions}
              onSubmit={handleSubmitClarification}
              isLoading={isSubmitting}
            />
          )}
      </div>
    </div>
  );
}
