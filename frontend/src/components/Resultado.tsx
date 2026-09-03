"use client";

import Gauge from "./Gauge";
import ActionCard from "./ActionCard";
import {
  RISK_COLOR,
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
