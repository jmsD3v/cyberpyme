export type AnswerValue = "yes" | "partial" | "no" | "unknown";
export type RiskLevel = "BAJO" | "MEDIO" | "ALTO" | "CRITICO";
export type Priority = "P1" | "P2" | "P3";

export interface Question {
  id: string;
  domain: string;
  question: string;
  weight: number;
  risk: string;
  nist: string[];
  cis: string[];
  recommendation_id: string;
  help: string;
}

export interface DomainLabel {
  label: string;
  domain_weight: number;
}

export interface PreguntasResponse {
  domains: Record<string, DomainLabel>;
  questions: Question[];
}

export interface DomainResult {
  domain: string;
  score: number;
  risk_level: RiskLevel;
}

export interface Action {
  title: string;
  domain: string;
  priority: Priority;
  impact: string;
  effort: string;
  time: string;
  why: string;
  steps: string[];
  question_id: string;
  risk: string;
}

export interface AssessmentResult {
  global_score: number;
  risk_level: RiskLevel;
  domains: Record<string, DomainResult>;
  top_actions: Action[];
}

export const RISK_COLOR: Record<RiskLevel, string> = {
  BAJO: "var(--color-status-bajo)",
  MEDIO: "var(--color-status-medio)",
  ALTO: "var(--color-status-alto)",
  CRITICO: "var(--color-status-critico)",
};

export const RISK_LABEL: Record<RiskLevel, string> = {
  BAJO: "Bajo",
  MEDIO: "Medio",
  ALTO: "Alto",
  CRITICO: "Crítico",
};

export const PRIORITY_LABEL: Record<Priority, string> = {
  P1: "Urgente",
  P2: "Importante",
  P3: "A planificar",
};
