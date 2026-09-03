"use server";

import { redirect } from "next/navigation";
import { revalidatePath } from "next/cache";
import { createClient } from "@/lib/supabase/server";

/** RLS ("owner actualiza su empresa") ya restringe esto al owner de la
 * propia empresa -- si el usuario no es owner, el update simplemente no
 * afecta ninguna fila. */
export async function actualizarNombreEmpresa(formData: FormData) {
  const nombre = String(formData.get("nombre") ?? "").trim();
  if (!nombre) {
    redirect(`/cuenta?error=${encodeURIComponent("Ingresá un nombre para tu empresa")}`);
  }

  const supabase = await createClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();
  const { data: perfil } = await supabase
    .from("perfiles")
    .select("empresa_id")
    .eq("id", user!.id)
    .maybeSingle();

  if (!perfil) {
    redirect(`/cuenta?error=${encodeURIComponent("No se pudo identificar tu empresa")}`);
  }

  const { error } = await supabase
    .from("empresas")
    .update({ nombre })
    .eq("id", perfil.empresa_id);

  if (error) {
    redirect(`/cuenta?error=${encodeURIComponent("No se pudo guardar el cambio. Probá de nuevo.")}`);
  }

  revalidatePath("/", "layout");
  redirect(`/cuenta?ok=1`);
}
