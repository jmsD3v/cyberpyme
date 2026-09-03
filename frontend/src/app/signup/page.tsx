import Link from "next/link";
import { signup } from "./actions";
import AuthShowcase from "@/components/AuthShowcase";

export default async function SignupPage({
  searchParams,
}: PageProps<"/signup">) {
  const params = await searchParams;
  const error = typeof params.error === "string" ? params.error : null;

  return (
    <div className="flex-1 flex flex-col lg:flex-row">
      <AuthShowcase />
      <div className="flex-1 flex items-center justify-center p-6 lg:border-l lg:border-border">
      <div className="w-full max-w-sm bg-surface border border-border rounded-2xl p-8">
        <h1 className="text-2xl font-bold mb-1">Creá tu empresa</h1>
        <p className="text-ink-muted text-sm mb-6">
          Un usuario por empresa, con su propio autodiagnóstico
        </p>

        {error && (
          <p className="mb-4 text-sm text-status-critico bg-status-critico/10 border border-status-critico/30 rounded-lg px-3 py-2">
            {error}
          </p>
        )}

        <form action={signup} className="space-y-4">
          <div>
            <label htmlFor="empresa" className="block text-sm text-ink-2 mb-1">Nombre de tu empresa</label>
            <input
              id="empresa"
              name="empresa"
              type="text"
              required
              placeholder="Ej: Ferretería Don José"
              className="w-full rounded-lg border border-border bg-card px-3 py-2 text-ink outline-none focus:border-accent"
            />
          </div>
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
            <label htmlFor="password" className="block text-sm text-ink-2 mb-1">Contraseña</label>
            <input
              id="password"
              name="password"
              type="password"
              required
              minLength={6}
              className="w-full rounded-lg border border-border bg-card px-3 py-2 text-ink outline-none focus:border-accent"
            />
          </div>
          <button
            type="submit"
            className="w-full rounded-full bg-accent text-white font-semibold py-2.5 hover:brightness-110 active:scale-[.98] transition"
          >
            Crear cuenta
          </button>
        </form>

        <p className="text-xs text-ink-muted mt-4 text-center">
          Al crear tu cuenta aceptás nuestros{" "}
          <Link href="/terminos" className="text-accent hover:underline">
            Términos de servicio
          </Link>{" "}
          y nuestra{" "}
          <Link href="/privacidad" className="text-accent hover:underline">
            Política de privacidad
          </Link>
          .
        </p>

        <p className="text-sm text-ink-muted mt-4 text-center">
          ¿Ya tenés cuenta?{" "}
          <Link href="/login" className="text-accent hover:underline">
            Iniciá sesión
          </Link>
        </p>
      </div>
      </div>
    </div>
  );
}
