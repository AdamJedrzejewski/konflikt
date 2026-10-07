export type ConflictClassification =
  | "brak_konfliktu"
  | "potencjalny_konflikt"
  | "wysoki_poziom_ryzyka"
  | "konflikt_oczywisty"
  | "UNCLEAR"
  | "UNKNOWN";

export type RiskLevel = "brak" | "niski" | "sredni" | "wysoki" | "krytyczny";

export type ConfidenceLevel = "wysoki" | "sredni" | "niski";

export type AnalysisCompleteness = "pelna" | "czesciowa" | "niedostateczna";

export type AnalysisStatus =
  | "pending"
  | "extracting"
  | "analyzing"
  | "complete"
  | "error";

export type AnalysisMode = "anchored" | "llm_only" | "error_fallback" | "knowledge_test";

export interface Entity {
  name: string;
  type: string;
}

export interface Role {
  entity: string;
  role: string;
}

export interface Relationship {
  from: string;
  to: string;
  type: string;
}

export interface AnalysisResult {
  model_connection?: { provider: string; model?: string };
  knowledge?: { version: string; concepts: number; records: number; mode: string; operator_status: string };
  knowledge_gaps?: string[];
  unassessed_scope?: string[];
  sources_used?: {
    id: string;
    claim: string;
    speaker?: string;
    limits?: string;
    evidence: { quote: string; source_key: string; source_id: string; line_start: number; line_end: number; source?: { text_path?: string } }[];
  }[];
  entities: Entity[];
  roles: Role[];
  relationships: Relationship[];
  matter_type: string;
  confidential_information_risk: string;
  adversity_risk: string;
  successive_representation_risk: string;
  organizational_barriers: string;
  missing_information: string[];
  analysis_completeness: AnalysisCompleteness;
  risk_level: RiskLevel;
  conflict_classification: ConflictClassification;
  justification: string;
  confidence_level: ConfidenceLevel;
  legal_basis?: string[];
  mode?: AnalysisMode;
  error?: { type: string; message: string };
}

export interface ClarificationQuestion {
  id: string;
  question: string;
}

export interface Analysis {
  id: string;
  status: AnalysisStatus;
  fact_pattern?: string;
  conflict_classification?: ConflictClassification;
  risk_level?: string;
  confidence_level?: string;
  final_result?: AnalysisResult;
  clarifying_questions?: ClarificationQuestion[];
  created_at: string;
}
