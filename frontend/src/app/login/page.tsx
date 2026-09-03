import Link from "next/link";
import { login } from "./actions";
import AuthShowcase from "@/components/AuthShowcase";

export default async function LoginPage({
  searchParams,
}: PageProps<"/login">) {
  const params = await searchParams;
  const error = typeof params.error === "string" ? params.error : null;

  return (
    <div className="flex-1 flex flex-col lg:flex-row">
      <AuthShowcase />
      <div className="flex-1 flex items-center justify-center p-6 lg:border-l lg:border-border">
      <div className="w-full max-w-sm bg-surface border border-border rounded-2xl p-8">
        <h1 className="text-2xl font-bold mb-1">Iniciá sesión</h1>
        <p className="text-ink-muted text-sm mb-6">Entrá para ver el estado de tu empresa</p>

        {error && (
          <p className="mb-4 text-sm text-status-critico bg-status-critico/10 border border-status-critico/30 rounded-lg px-3 py-2">
            {error}
          </p>
        )}

        <form action={login} className="space-y-4">
          <div>
            <label htmlFor="email" className="block text-sm text-ink-2 mb-1">Email</label>
            <input
              id="email"
              name="email"
              type="email"
              required
              className="w-full rounded-lg border border-border bg-card px-3 py-2 text-ink outline-none focus:border-accent"
            />
          </div>
          <div>
            <div className="flex items-center justify-between mb-1">
              <label htmlFor="password" className="block text-sm text-ink-2">Contraseña</label>
              <Link href="/forgot-password" className="text-xs text-accent hover:underline">
                ¿Olvidaste tu contraseña?
              </Link>
            </div>
            <input
              id="password"
              name="password"
              type="password"
              required
              className="w-full rounded-lg border border-border bg-card px-3 py-2 text-ink outline-none focus:border-accent"
            />
          </div>
          <button
            type="submit"
            className="w-full rounded-full bg-accent text-white font-semibold py-2.5 hover:brightness-110 active:scale-[.98] transition"
          >
            Entrar
          </button>
        </form>

        <p className="text-sm text-ink-muted mt-6 text-center">
          ¿No tenés cuenta?{" "}
          <Link href="/signup" className="text-accent hover:underline">
            Creá tu empresa
          </Link>
        </p>
      </div>
      </div>
    </div>
  );
}
