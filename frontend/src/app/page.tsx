import Link from "next/link";
import AppShell from "@/components/AppShell";
import { createClient } from "@/lib/supabase/server";
import { completarRegistro } from "./onboarding-actions";
import { RISK_COLOR, RISK_LABEL, type RiskLevel } from "@/lib/types";

interface Evaluacion {
  id: string;
  global_score: number;
  risk_level: RiskLevel;
  created_at: string;
}

export default async function DashboardPage() {
  const supabase = await createClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();

  if (!user) {
    // El proxy ya deberia haber redirigido a /login -- resguardo extra.
    return null;
  }

  const { data: perfil } = await supabase
    .from("perfiles")
    .select("empresa_id, empresas(nombre)")
    .eq("id", user.id)
    .maybeSingle();

  if (!perfil) {
    return (
      <div className="flex-1 flex items-center justify-center p-6">
        <div className="w-full max-w-sm bg-surface border border-border rounded-2xl p-8">
          <h1 className="text-xl font-bold mb-1">Un último paso</h1>
          <p className="text-ink-muted text-sm mb-6">
            Confirmaste tu email — ahora contanos el nombre de tu empresa para
            terminar de crear tu cuenta.
          </p>
          <form action={completarRegistro} className="space-y-4">
            <input
              name="empresa"
              type="text"
              required
              placeholder="Ej: Ferretería Don José"
              className="w-full rounded-lg border border-border bg-card px-3 py-2 text-ink outline-none focus:border-accent"
            />
            <button
              type="submit"
              className="w-full rounded-full bg-accent text-white font-semibold py-2.5 hover:brightness-110 active:scale-[.98] transition"
            >
              Continuar
            </button>
          </form>
        </div>
      </div>
    );
  }

  const empresaNombre = (perfil.empresas as unknown as { nombre: string } | null)?.nombre;

  const { data: evaluaciones } = await supabase
    .from("evaluaciones")
    .select("id, global_score, risk_level, created_at")
    .order("created_at", { ascending: false });

  return (
    <AppShell empresa={empresaNombre}>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-xl font-bold">Tus evaluaciones</h1>
        <Link
          href="/cuestionario"
          className="rounded-full bg-accent text-white text-sm font-semibold px-4 py-2 hover:brightness-110 active:scale-[.98] transition"
        >
          + Nueva evaluación
        </Link>
      </div>

      {!evaluaciones || evaluaciones.length === 0 ? (
        <div className="bg-surface border border-border rounded-2xl p-8 text-center">
          <p className="text-ink-2">Todavía no hiciste ninguna evaluación.</p>
          <Link href="/cuestionario" className="inline-block mt-3 text-accent hover:underline text-sm">
            Empezar el autodiagnóstico →
          </Link>
        </div>
      ) : (
        <div className="bg-surface border border-border rounded-2xl divide-y divide-border">
          {(evaluaciones as Evaluacion[]).map((ev) => (
            <div key={ev.id} className="flex items-center justify-between px-5 py-4">
              <div>
                <p className="text-sm text-ink-2">
                  {new Date(ev.created_at).toLocaleDateString("es-AR", {
                    day: "2-digit",
                    month: "long",
                    year: "numeric",
                  })}
                </p>
                <p className="font-semibold">{Math.round(ev.global_score)}/100</p>
              </div>
              <span
                className="text-xs font-bold text-white px-3 py-1 rounded-full"
                style={{ background: RISK_COLOR[ev.risk_level] }}
              >
                Riesgo {RISK_LABEL[ev.risk_level]}
              </span>
            </div>
          ))}
        </div>
      )}
    </AppShell>
  );
}
