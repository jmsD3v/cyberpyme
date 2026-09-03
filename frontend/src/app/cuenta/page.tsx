import { redirect } from "next/navigation";
import Link from "next/link";
import AppShell from "@/components/AppShell";
import { createClient } from "@/lib/supabase/server";
import { actualizarNombreEmpresa } from "./actions";

export default async function CuentaPage({ searchParams }: PageProps<"/cuenta">) {
  const params = await searchParams;
  const error = typeof params.error === "string" ? params.error : null;
  const ok = params.ok === "1";

  const supabase = await createClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();
  if (!user) redirect("/login");

  const { data: perfil } = await supabase
    .from("perfiles")
    .select("rol, empresas(nombre)")
    .eq("id", user.id)
    .maybeSingle();

  if (!perfil) redirect("/");

  const empresaNombre = perfil.empresas?.nombre ?? "";
  const esOwner = perfil.rol === "owner";

  return (
    <AppShell empresa={empresaNombre}>
      <h1 className="text-xl font-bold mb-6">Cuenta</h1>

      <div className="space-y-6 max-w-md">
        <section className="bg-surface border border-border rounded-2xl p-6">
          <h2 className="font-semibold mb-1">Empresa</h2>
          <p className="text-sm text-ink-muted mb-4">
            {esOwner
              ? "Este nombre aparece en el encabezado y en tus informes."
              : "Solo el owner de la empresa puede cambiar este nombre."}
          </p>

          {error && (
            <p className="mb-4 text-sm text-status-critico bg-status-critico/10 border border-status-critico/30 rounded-lg px-3 py-2">
              {error}
            </p>
          )}
          {ok && (
            <p className="mb-4 text-sm text-status-bajo bg-status-bajo/10 border border-status-bajo/30 rounded-lg px-3 py-2">
              Nombre actualizado.
            </p>
          )}

          <form action={actualizarNombreEmpresa} className="flex gap-2">
            <input
              name="nombre"
              type="text"
              required
              defaultValue={empresaNombre}
              disabled={!esOwner}
              className="flex-1 rounded-lg border border-border bg-card px-3 py-2 text-ink outline-none focus:border-accent disabled:opacity-60"
            />
            {esOwner && (
              <button
                type="submit"
                className="rounded-full bg-accent text-white text-sm font-semibold px-4 hover:brightness-110 active:scale-[.98] transition"
              >
                Guardar
              </button>
            )}
          </form>
        </section>

        <section className="bg-surface border border-border rounded-2xl p-6">
          <h2 className="font-semibold mb-1">Datos de acceso</h2>
          <p className="text-sm text-ink-muted mb-4">{user.email}</p>
          <Link href="/forgot-password" className="text-sm text-accent hover:underline">
            Cambiar mi contraseña
          </Link>
        </section>
      </div>
    </AppShell>
  );
}
