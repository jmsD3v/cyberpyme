"use server";

import { revalidatePath } from "next/cache";
import { createClient } from "@/lib/supabase/server";

/** Completa el alta cuando el usuario confirmo el email y entro sin haber
 * podido crear su empresa en el momento del signup (ver signup/actions.ts). */
export async function completarRegistro(formData: FormData) {
  const empresa = String(formData.get("empresa") ?? "").trim();
  if (!empresa) return;

  const supabase = await createClient();
  const { error } = await supabase.rpc("crear_empresa", { p_nombre: empresa });
  if (error) throw new Error(error.message);

  revalidatePath("/");
}
