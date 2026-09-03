"use client";

import { useEffect, useState } from "react";
import { createClient } from "@/lib/supabase/client";
import Resultado from "./Resultado";
import type { AnswerValue, AssessmentResult, PreguntasResponse } from "@/lib/types";
import type { Json } from "@/lib/supabase/database.types";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
const OPCIONES: { value: AnswerValue; label: string }[] = [
  { value: "yes", label: "Sí" },
  { value: "partial", label: "Parcial" },
  { value: "no", label: "No" },
  { value: "unknown", label: "No sé" },
];

export default function Cuestionario({ empresa }: { empresa: string }) {
  const [catalogo, setCatalogo] = useState<PreguntasResponse | null>(null);
  const [domainIndex, setDomainIndex] = useState(0);
  const [answers, setAnswers] = useState<Record<string, AnswerValue>>({});
  const [result, setResult] = useState<AssessmentResult | null>(null);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch(`${API_URL}/preguntas`)
      .then((r) => r.json())
      .then(setCatalogo)
      .catch(() => setError("No se pudo conectar con la API. ¿Está corriendo en el puerto 8000?"));
  }, []);

  if (error) {
    return <p className="text-status-critico">{error}</p>;
  }

  if (!catalogo) {
    return <p className="text-ink-muted">Cargando cuestionario…</p>;
  }

  if (result) {
    return <Resultado result={result} catalogo={catalogo} empresa={empresa} />;
  }

  const domainOrder = Object.keys(catalogo.domains);
  const domain = domainOrder[domainIndex];
  const preguntas = catalogo.questions.filter((q) => q.domain === domain);
  const completo = preguntas.every((q) => answers[q.id] !== undefined);
  const esUltimo = domainIndex === domainOrder.length - 1;

  async function siguiente() {
    if (!esUltimo) {
      setDomainIndex((i) => i + 1);
      return;
    }
    setSaving(true);
    try {
      const res = await fetch(`${API_URL}/evaluar`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ respuestas: answers }),
      });
      if (!res.ok) throw new Error("No se pudo calcular el resultado");
      const data: AssessmentResult = await res.json();

      const supabase = createClient();
      const {
        data: { user },
      } = await supabase.auth.getUser();
      const { data: perfil } = await supabase
        .from("perfiles")
        .select("empresa_id")
        .eq("id", user!.id)
        .single();

      const { error: insertError } = await supabase.from("evaluaciones").insert({
        empresa_id: perfil!.empresa_id,
        created_by: user!.id,
        respuestas: answers,
        global_score: data.global_score,
        risk_level: data.risk_level,
        domains: data.domains as unknown as Json,
      });
      if (insertError) throw insertError;

      setResult(data);
    } catch {
      setError("Hubo un problema al guardar la evaluación. Probá de nuevo.");
    } finally {
      setSaving(false);
    }
  }

  const progresoPct = Math.round((domainIndex / domainOrder.length) * 100);

  return (
    <div>
      <div className="flex justify-center gap-2.5 mb-4">
        {domainOrder.map((d, i) => (
          <div
            key={d}
            title={catalogo.domains[d].label}
            className={`w-8 h-8 rounded-full border-2 flex items-center justify-center text-xs font-bold transition ${
              i === domainIndex
                ? "border-accent bg-accent/20 scale-110"
                : i < domainIndex
                  ? "border-accent bg-accent/10 text-accent"
                  : "border-border text-ink-muted opacity-50"
            }`}
          >
            {i + 1}
          </div>
        ))}
      </div>

      <div className="mb-5">
        <div className="flex justify-between text-sm text-ink-2 mb-2">
          <span>{catalogo.domains[domain].label}</span>
          <span>
            Dominio {domainIndex + 1} de {domainOrder.length}
          </span>
        </div>
        <div className="h-1.5 bg-track rounded-full overflow-hidden">
          <div
            className="h-full bg-accent rounded-full transition-all duration-300"
            style={{ width: `${progresoPct}%` }}
          />
        </div>
      </div>

      <div className="bg-surface border border-border rounded-2xl divide-y divide-border">
        {preguntas.map((q) => (
          <div key={q.id} className="px-5 py-4">
            <p className="mb-1.5">{q.question}</p>
            {q.help && (
              <p className="text-xs text-ink-muted mb-3 flex gap-1.5">
                <span>💡</span>
                <span>{q.help}</span>
              </p>
            )}
            <div className="flex gap-2 flex-wrap">
              {OPCIONES.map((opt) => (
                <button
                  key={opt.value}
                  type="button"
                  onClick={() => setAnswers((a) => ({ ...a, [q.id]: opt.value }))}
                  className={`px-4 py-2 rounded-full text-sm border transition ${
                    answers[q.id] === opt.value
                      ? "bg-accent border-accent text-white font-semibold"
                      : "bg-card border-border text-ink-2 hover:border-accent"
                  }`}
                >
                  {opt.label}
                </button>
              ))}
            </div>
          </div>
        ))}
      </div>

      <div className="mt-6">
        {!completo && (
          <p className="text-xs text-ink-muted text-center mb-3">
            Respondé todas las preguntas para continuar
          </p>
        )}
        <div className="flex items-center justify-between">
          <button
            type="button"
            disabled={domainIndex === 0}
            onClick={() => setDomainIndex((i) => i - 1)}
            className="rounded-full bg-track px-5 py-2.5 font-semibold disabled:opacity-40"
          >
            Anterior
          </button>
          <button
            type="button"
            disabled={!completo || saving}
            onClick={siguiente}
            className="rounded-full bg-accent text-white px-5 py-2.5 font-semibold disabled:opacity-40 hover:brightness-110 active:scale-[.98] transition"
          >
            {saving ? "Calculando…" : esUltimo ? "Ver resultado" : "Siguiente"}
          </button>
        </div>
      </div>
    </div>
  );
}
