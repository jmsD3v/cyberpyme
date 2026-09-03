import { redirect } from "next/navigation";
import AppShell from "@/components/AppShell";
import EvaluacionDetalle from "@/components/EvaluacionDetalle";
import DeleteEvaluacionButton from "@/components/DeleteEvaluacionButton";
import { createClient } from "@/lib/supabase/server";
import type { AnswerValue } from "@/lib/types";
import { deleteEvaluacion } from "./actions";

export default async function EvaluacionDetallePage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;

  const supabase = await createClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();
  if (!user) redirect("/login");

  const { data: perfil } = await supabase
    .from("perfiles")
    .select("empresas(nombre)")
    .eq("id", user.id)
    .maybeSingle();

  if (!perfil) redirect("/");

  // RLS ya restringe esto a evaluaciones de la propia empresa -- si no
  // aparece, o no existe o no es tuya, en ambos casos volvemos al dashboard.
  const { data: evaluacion } = await supabase
    .from("evaluaciones")
    .select("respuestas, created_at")
    .eq("id", id)
    .maybeSingle();

  if (!evaluacion) redirect("/");

  const empresaNombre = perfil.empresas?.nombre ?? "tu empresa";
  const fecha = new Date(evaluacion.created_at).toLocaleDateString("es-AR", {
    day: "2-digit",
    month: "long",
    year: "numeric",
  });

  return (
    <AppShell empresa={empresaNombre}>
      <EvaluacionDetalle
        respuestas={evaluacion.respuestas as Record<string, AnswerValue>}
        empresa={empresaNombre}
        fecha={fecha}
      />
      <div className="mt-8 flex justify-end no-print">
        <DeleteEvaluacionButton action={deleteEvaluacion.bind(null, id)} />
      </div>
    </AppShell>
  );
}
