import type { Analysis } from "../types/analysis";

// Strona i API pod jednym adresem: Next.js przekazuje /api/v1 do backendu (next.config.ts).
const API_BASE = process.env.NEXT_PUBLIC_API_URL || "/api/v1";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    credentials: "include",
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) {
    const body = await res.json().catch(() => null);

    // FastAPI validation error (422) — extract human-readable messages
    if (res.status === 422 && body?.detail && Array.isArray(body.detail)) {
      const messages = body.detail.map(
        (e: { msg?: string }) => e.msg || "Błąd walidacji"
      );
      throw new Error(messages.join("; "));
    }

    if (res.status === 401) {
      throw new Error("Brak logowania albo sesja wygasła. Odśwież stronę, aby zalogować się ponownie.");
    }

    // Other structured errors (e.g. 400, 404)
    if (body?.detail && typeof body.detail === "string") {
      throw new Error(body.detail);
    }

    throw new Error(`Błąd serwera (${res.status})`);
  }
  return res.json() as Promise<T>;
}

export async function createAnalysis(factPattern: string) {
  return request<Analysis>("/analyze", {
    method: "POST",
    body: JSON.stringify({ fact_pattern: factPattern }),
  });
}

export async function getAnalysis(id: string) {
  return request<Analysis>(`/analyze/${id}`);
}

export async function submitClarification(
  analysisId: string,
  answers: { question_id: string; answer: string }[]
) {
  return request<{ status: string; message: string }>(
    `/analyze/${analysisId}/clarify`,
    {
      method: "POST",
      body: JSON.stringify({ analysis_id: analysisId, answers }),
    }
  );
}

export async function getHistory() {
  return request<{ items: Analysis[]; total: number }>("/history");
}

export type Me = { email: string; role: "operator" | "tester" };

export async function getMe() {
  return request<Me>("/me");
}

export type FeedbackKind = "wynik" | "podstawa" | "wyjasnienie" | "fakty" | "techniczny" | "inne";

export const FEEDBACK_KIND_LABELS: Record<FeedbackKind, string> = {
  wynik: "Błędna ocena konfliktu",
  podstawa: "Brak lub błąd podstawy (przepis, orzeczenie, komentarz)",
  wyjasnienie: "Niejasne lub niepełne wyjaśnienie",
  fakty: "Pominięty fakt albo brakujące pytanie",
  techniczny: "Błąd techniczny",
  inne: "Inne",
};

export type Feedback = {
  id: number;
  number: string;
  analysis_id: string;
  author_email: string;
  created_at: string;
  kind: FeedbackKind;
  description: string;
  expected: string | null;
  source: string | null;
  app_version: string;
  knowledge_version: string | null;
  status: string;
};

export async function createFeedback(
  analysisId: string,
  body: { kind: FeedbackKind; description: string; expected?: string; source?: string }
) {
  return request<Feedback>(`/analyze/${analysisId}/feedback`, {
    method: "POST",
    body: JSON.stringify(body),
  });
}

export async function getAnalysisFeedback(analysisId: string) {
  return request<Feedback[]>(`/analyze/${analysisId}/feedback`);
}

export async function getFeedback() {
  return request<Feedback[]>("/feedback");
}

export const FEEDBACK_EXPORT_URL = `${API_BASE}/feedback/export.csv`;
