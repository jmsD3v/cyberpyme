"use client";

import { useEffect, useState } from "react";
import Resultado from "./Resultado";
import type { AnswerValue, AssessmentResult, PreguntasResponse } from "@/lib/types";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export default function EvaluacionDetalle({
  respuestas,
  empresa,
  fecha,
}: {
  respuestas: Record<string, AnswerValue>;
  empresa: string;
  fecha: string;
}) {
  const [catalogo, setCatalogo] = useState<PreguntasResponse | null>(null);
  const [result, setResult] = useState<AssessmentResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([
      fetch(`${API_URL}/preguntas`).then((r) => r.json()),
      fetch(`${API_URL}/evaluar`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ respuestas }),
      }).then((r) => r.json()),
    ])
      .then(([catalogoRes, resultRes]) => {
        setCatalogo(catalogoRes);
        setResult(resultRes);
      })
      .catch(() => setError("No se pudo conectar con la API. ¿Está corriendo en el puerto 8000?"));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  if (error) {
    return <p className="text-status-critico">{error}</p>;
  }

  if (!catalogo || !result) {
    return <p className="text-ink-muted">Cargando evaluación…</p>;
  }

  return <Resultado result={result} catalogo={catalogo} empresa={empresa} fecha={fecha} />;
}
