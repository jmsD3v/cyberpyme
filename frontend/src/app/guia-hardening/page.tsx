import { redirect } from "next/navigation";
import AppShell from "@/components/AppShell";
import GuiaHardening from "@/components/GuiaHardening";
import { createClient } from "@/lib/supabase/server";

export default async function GuiaHardeningPage() {
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

  const empresaNombre = perfil.empresas?.nombre ?? "tu empresa";

  return (
    <AppShell empresa={empresaNombre}>
      <GuiaHardening />
    </AppShell>
  );
}
