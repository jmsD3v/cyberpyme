import { redirect } from "next/navigation";
import AppShell from "@/components/AppShell";
import Cuestionario from "@/components/Cuestionario";
import { createClient } from "@/lib/supabase/server";

export default async function CuestionarioPage() {
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

  const empresaNombre = (perfil.empresas as unknown as { nombre: string } | null)?.nombre ?? "tu empresa";

  return (
    <AppShell empresa={empresaNombre}>
      <Cuestionario empresa={empresaNombre} />
    </AppShell>
  );
}
