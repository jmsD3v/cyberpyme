"use client";

import { useState, type FormEvent } from "react";
import Link from "next/link";
import { createClient } from "@/lib/supabase/client";
import { translateAuthError } from "@/lib/auth-errors";
import AuthShowcase from "@/components/AuthShowcase";

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState("");
  const [sent, setSent] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(null);
    const supabase = createClient();
    const { error } = await supabase.auth.resetPasswordForEmail(email, {
      redirectTo: `${window.location.origin}/reset-password`,
    });
    setLoading(false);
    if (error) {
      setError(translateAuthError(error.message));
      return;
    }
    setSent(true);
  }

  return (
    <div className="flex-1 flex flex-col lg:flex-row">
      <AuthShowcase />
      <div className="flex-1 flex items-center justify-center p-6 lg:border-l lg:border-border">
        {sent ? (
          <div className="max-w-sm text-center">
            <div className="text-4xl mb-3">📬</div>
            <h1 className="text-xl font-bold mb-2">Revisá tu email</h1>
            <p className="text-ink-2 text-sm">
              Si existe una cuenta con ese email, te mandamos un link para
              elegir una nueva contraseña.
            </p>
            <Link href="/login" className="inline-block mt-6 text-accent hover:underline text-sm">
              Volver a iniciar sesión
            </Link>
          </div>
        ) : (
          <div className="w-full max-w-sm bg-surface border border-border rounded-2xl p-8">
            <h1 className="text-2xl font-bold mb-1">Recuperar contraseña</h1>
            <p className="text-ink-muted text-sm mb-6">
              Ingresá tu email y te mandamos un link para elegir una nueva contraseña.
            </p>

            {error && (
              <p className="mb-4 text-sm text-status-critico bg-status-critico/10 border border-status-critico/30 rounded-lg px-3 py-2">
                {error}
              </p>
            )}

            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label htmlFor="email" className="block text-sm text-ink-2 mb-1">Email</label>
                <input
                  id="email"
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full rounded-lg border border-border bg-card px-3 py-2 text-ink outline-none focus:border-accent"
                />
              </div>
              <button
                type="submit"
                disabled={loading}
                className="w-full rounded-full bg-accent text-white font-semibold py-2.5 hover:brightness-110 active:scale-[.98] transition disabled:opacity-60"
              >
                {loading ? "Enviando…" : "Enviar link"}
              </button>
            </form>

            <p className="text-sm text-ink-muted mt-6 text-center">
              <Link href="/login" className="text-accent hover:underline">
                Volver a iniciar sesión
              </Link>
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
