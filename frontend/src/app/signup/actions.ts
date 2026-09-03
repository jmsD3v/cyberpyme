"use server";

import { redirect } from "next/navigation";
import { createClient } from "@/lib/supabase/server";
import { translateAuthError } from "@/lib/auth-errors";

export async function signup(formData: FormData) {
  const empresa = String(formData.get("empresa") ?? "").trim();
  const email = String(formData.get("email") ?? "");
  const password = String(formData.get("password") ?? "");

  if (!empresa) {
    redirect(`/signup?error=${encodeURIComponent("Ingresá el nombre de tu empresa")}`);
  }

  const supabase = await createClient();

  const { data, error: signUpError } = await supabase.auth.signUp({ email, password });
  if (signUpError) {
    redirect(`/signup?error=${encodeURIComponent(translateAuthError(signUpError.message))}`);
  }

  // Si el proyecto tiene confirmacion de email activada, signUp NO deja
  // sesion activa todavia -- no se puede llamar crear_empresa como anon
  // (revocado a proposito, ver migracion "revocar_public_en_empresa_actual").
  // El alta de empresa/perfil se completa recien cuando confirme el mail
  // y entre por /login.
  if (!data.session) {
    redirect("/signup/revisa-tu-email");
  }

  // Sesion activa de una: crear_empresa corre como el usuario recien
  // creado, atomico (empresa + perfil owner en la misma transaccion, ver
  // migracion "esquema_inicial_multiempresa").
  const { error: rpcError } = await supabase.rpc("crear_empresa", { p_nombre: empresa });
  if (rpcError) {
    redirect(`/signup?error=${encodeURIComponent("No se pudo crear tu empresa. Probá de nuevo en unos minutos.")}`);
  }

  redirect("/");
}
