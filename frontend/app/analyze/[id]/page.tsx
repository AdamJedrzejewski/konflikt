"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { getAnalysis, submitClarification } from "@/lib/api";
import type { Analysis } from "@/types/analysis";
import { LoadingSpinner } from "@/components/ui/LoadingSpinner";
import { ClarificationForm } from "@/components/ui/ClarificationForm";

export default function AnalysisStatusPage() {
  const { id } = useParams<{ id: string }>();
  const router = useRouter();
  const [analysis, setAnalysis] = useState<Analysis | null>(null);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    const poll = async () => {
      const data = await getAnalysis(id);
      setAnalysis(data);
      if (data.status === "complete") {
        clearInterval(interval);
        // Has clarifying questions → stay on this page to show them
        if (!data.clarifying_questions?.length) {
          router.replace(`/analyze/${id}/result`);
        }
      } else if (data.status === "error") {
        clearInterval(interval);
      }
    };

    const interval = setInterval(poll, 2500);
    poll();
    return () => clearInterval(interval);
  }, [id, router]);

  const handleClarification = async (answers: { question_id: string; answer: string }[]) => {
    setSubmitting(true);
    await submitClarification(id, answers);
    router.replace(`/analyze/${id}/result`);
  };

  if (!analysis || (analysis.status !== "complete" && analysis.status !== "error")) {
    return (
      <div className="flex flex-col items-center justify-center py-24 space-y-4">
        <LoadingSpinner />
        <p className="text-ink-muted text-sm">
          {analysis?.status === "extracting" ? "Analizuję stan faktyczny..." : "Przetwarzanie analizy..."}
        </p>
      </div>
    );
  }

  if (analysis.status === "error") {
    return (
      <div className="max-w-lg mx-auto py-20 text-center space-y-4">
        <p className="text-red-600 font-medium">Wystąpił błąd podczas analizy.</p>
        <button onClick={() => router.push("/analyze")} className="text-sm text-primary hover:underline">
          ← Spróbuj ponownie
        </button>
      </div>
    );
  }

  if (analysis.clarifying_questions?.length) {
    return (
      <div className="max-w-2xl mx-auto px-4 py-10">
        <h1 className="text-xl font-semibold text-ink mb-2">Pytania uzupełniające</h1>
        <p className="text-sm text-ink-muted mb-6">
          System potrzebuje dodatkowych informacji. Odpowiedzi są opcjonalne.
        </p>
        <ClarificationForm
          questions={analysis.clarifying_questions}
          onSubmit={handleClarification}
          isLoading={submitting}
        />
      </div>
    );
  }

  return null;
}
