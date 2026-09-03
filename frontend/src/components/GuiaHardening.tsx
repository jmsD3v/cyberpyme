"use client";

import { useEffect, useState } from "react";
import ActionCard from "./ActionCard";
import type { Action, PreguntasResponse } from "@/lib/types";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export default function GuiaHardening() {
  const [catalogo, setCatalogo] = useState<PreguntasResponse | null>(null);
  const [acciones, setAcciones] = useState<Action[] | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([
      fetch(`${API_URL}/preguntas`).then((r) => r.json()),
      fetch(`${API_URL}/guia-hardening`).then((r) => r.json()),
    ])
      .then(([catalogoRes, accionesRes]) => {
        setCatalogo(catalogoRes);
        setAcciones(accionesRes);
      })
      .catch(() => setError("No se pudo conectar con la API. ¿Está corriendo en el puerto 8000?"));
  }, []);

  if (error) {
    return <p className="text-status-critico">{error}</p>;
  }

  if (!catalogo || !acciones) {
    return <p className="text-ink-muted">Cargando guía de hardening…</p>;
  }

  const questionById = Object.fromEntries(catalogo.questions.map((q) => [q.id, q]));
  const byDomain: Record<string, Action[]> = {};
  for (const a of acciones) {
    (byDomain[a.domain] ??= []).push(a);
  }

  return (
    <div>
      <h1 className="text-xl font-bold mb-1">Guía de hardening completa</h1>
      <p className="text-ink-muted text-sm mb-8">
        Las {acciones.length} acciones recomendadas por la metodología NIST CSF 2.0 + CIS Controls
        v8.1 IG1, agrupadas por dominio y ordenadas por prioridad — no depende de ningún
        autodiagnóstico puntual, es el catálogo completo.
      </p>

      <div className="space-y-8">
        {Object.entries(catalogo.domains).map(([domain, info]) => {
          const domainActions = byDomain[domain] ?? [];
          if (domainActions.length === 0) return null;
          return (
            <section key={domain}>
              <h2 className="font-semibold mb-3 flex items-center gap-2">
                {info.label}
                <span className="text-xs font-normal text-ink-muted bg-track px-2 py-0.5 rounded-full">
                  {domainActions.length} acciones
                </span>
              </h2>
              <div className="space-y-2">
                {domainActions.map((action, i) => (
                  <ActionCard
                    key={action.question_id}
                    action={action}
                    question={questionById[action.question_id]}
                    domainLabel={info.label}
                    index={i}
                  />
                ))}
              </div>
            </section>
          );
        })}
      </div>
    </div>
  );
}
