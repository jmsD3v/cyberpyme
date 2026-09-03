"use client";

import { useState } from "react";
import Gauge from "./Gauge";
import {
  RISK_COLOR,
  PRIORITY_LABEL,
  type AssessmentResult,
  type PreguntasResponse,
} from "@/lib/types";

export default function Resultado({
  result,
  catalogo,
  empresa,
}: {
  result: AssessmentResult;
  catalogo: PreguntasResponse;
  empresa: string;
}) {
  const questionById = Object.fromEntries(catalogo.questions.map((q) => [q.id, q]));

  return (
    <div className="space-y-8">
      <div className="bg-surface border border-border rounded-2xl p-8 flex flex-wrap items-center gap-8">
        <Gauge score={result.global_score} riskLevel={result.risk_level} />
        <div>
          <h1 className="text-xl font-bold">Informe de autodiagnóstico — {empresa}</h1>
          <p className="text-ink-muted text-sm mt-1">
            Metodología NIST CSF 2.0 + CIS Controls v8.1 IG1
          </p>
        </div>
      </div>

      <section>
        <h2 className="font-semibold mb-3">Score por dominio</h2>
        <div className="bg-surface border border-border rounded-2xl p-6 space-y-3">
          {catalogo.domains &&
            Object.entries(result.domains).map(([domain, r]) => (
              <div key={domain} className="flex items-center gap-3">
                <span className="w-40 text-sm text-ink-2 shrink-0">
                  {catalogo.domains[domain]?.label ?? domain}
                </span>
                <div className="flex-1 h-4 bg-track rounded-full overflow-hidden">
                  <div
                    className="h-full rounded-full transition-all duration-700"
                    style={{ width: `${r.score}%`, background: RISK_COLOR[r.risk_level] }}
                  />
                </div>
                <span className="w-8 text-right text-sm font-semibold">{Math.round(r.score)}</span>
              </div>
            ))}
        </div>
      </section>

      <section>
        <h2 className="font-semibold mb-3">Acciones priorizadas — cómo resolver cada brecha</h2>
        {result.top_actions.length === 0 ? (
          <div className="bg-surface border border-border rounded-2xl p-6 text-ink-2">
            Sin brechas detectadas: todas las respuestas están en línea con la metodología. 🎉
          </div>
        ) : (
          <div className="space-y-2">
            {result.top_actions.map((action, i) => (
              <ActionCard
                key={`${action.question_id}-${i}`}
                action={action}
                question={questionById[action.question_id]}
                domainLabel={catalogo.domains[action.domain]?.label ?? action.domain}
                index={i}
              />
            ))}
          </div>
        )}
      </section>
    </div>
  );
}

function ActionCard({
  action,
  question,
  domainLabel,
  index,
}: {
  action: AssessmentResult["top_actions"][number];
  question?: PreguntasResponse["questions"][number];
  domainLabel: string;
  index: number;
}) {
  const [open, setOpen] = useState(false);
  const badgeColor =
    action.priority === "P1" ? "bg-status-critico" : action.priority === "P2" ? "bg-status-medio text-[#3a2a00]" : "bg-ink-muted";

  return (
    <article
      className="bg-surface border border-border rounded-2xl overflow-hidden animate-[cardIn_.4s_ease_both]"
      style={{ animationDelay: `${index * 60}ms` }}
    >
      <button
        type="button"
        onClick={() => setOpen((o) => !o)}
        className="w-full text-left px-5 py-4 flex flex-wrap items-center gap-3"
      >
        <span className={`text-xs font-bold text-white px-2.5 py-1 rounded-full ${badgeColor}`}>
          {PRIORITY_LABEL[action.priority]}
        </span>
        <span className="font-semibold flex-1 min-w-[200px]">{action.title}</span>
        <span className="flex gap-1.5 flex-wrap text-xs text-ink-muted">
          <span className="bg-track px-2 py-0.5 rounded-full">Dominio: {domainLabel}</span>
          <span className="bg-track px-2 py-0.5 rounded-full">Impacto: {action.impact}</span>
          <span className="bg-track px-2 py-0.5 rounded-full">Esfuerzo: {action.effort}</span>
          <span className="bg-track px-2 py-0.5 rounded-full">Tiempo: {action.time}</span>
        </span>
        <span className={`text-ink-muted transition-transform ${open ? "rotate-180" : ""}`}>▾</span>
      </button>
      {open && (
        <div className="px-5 pb-5 border-t border-border pt-4">
          <p className="italic text-ink-2 mb-3">{action.why}</p>
          <ol className="list-decimal pl-5 space-y-1.5">
            {action.steps.map((s, i) => (
              <li key={i}>{s}</li>
            ))}
          </ol>
          {question && (
            <p className="text-xs text-ink-muted mt-3">
              Basado en la pregunta: &ldquo;{question.question}&rdquo; — NIST CSF:{" "}
              {question.nist.join(", ")} · CIS IG1: {question.cis.join(", ")}
            </p>
          )}
        </div>
      )}
    </article>
  );
}
