"use client";

import { useState } from "react";
import { PRIORITY_LABEL, type Action, type Question } from "@/lib/types";

export default function ActionCard({
  action,
  question,
  domainLabel,
  index,
}: {
  action: Action;
  question?: Question;
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
