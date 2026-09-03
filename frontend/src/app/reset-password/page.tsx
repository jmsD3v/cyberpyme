"use client";

import { useEffect, useState, type FormEvent } from "react";
import { useRouter } from "next/navigation";
import { createClient } from "@/lib/supabase/client";
import { translateAuthError } from "@/lib/auth-errors";
import AuthShowcase from "@/components/AuthShowcase";

export default function ResetPasswordPage() {
  const router = useRouter();
  const [ready, setReady] = useState(false);
  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const supabase = createClient();
    const {
      data: { subscription },
    } = supabase.auth.onAuthStateChange((event) => {
      if (event === "PASSWORD_RECOVERY") setReady(true);
    });
    // Si la sesion de recuperacion ya estaba activa al montar (ej. recarga de pagina), tambien la aceptamos.
    supabase.auth.getSession().then(({ data: { session } }) => {
      if (session) setReady(true);
    });
    return () => subscription.unsubscribe();
  }, []);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    if (password !== confirm) {
      setError("Las contraseñas no coinciden.");
      return;
    }
    setLoading(true);
    setError(null);
    const supabase = createClient();
    const { error } = await supabase.auth.updateUser({ password });
    setLoading(false);
    if (error) {
      setError(translateAuthError(error.message));
      return;
    }
    router.push("/");
  }

  if (!ready) {
    return (
      <div className="flex-1 flex items-center justify-center p-6 text-center">
        <p className="text-ink-muted text-sm">Verificando el link…</p>
      </div>
    );
  }

  return (
    <div className="flex-1 flex flex-col lg:flex-row">
      <AuthShowcase />
      <div className="flex-1 flex items-center justify-center p-6 lg:border-l lg:border-border">
        <div className="w-full max-w-sm bg-surface border border-border rounded-2xl p-8">
          <h1 className="text-2xl font-bold mb-1">Elegí una nueva contraseña</h1>
          <p className="text-ink-muted text-sm mb-6">Esto reemplaza tu contraseña anterior.</p>

          {error && (
            <p className="mb-4 text-sm text-status-critico bg-status-critico/10 border border-status-critico/30 rounded-lg px-3 py-2">
              {error}
            </p>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label htmlFor="password" className="block text-sm text-ink-2 mb-1">Nueva contraseña</label>
              <input
                id="password"
                type="password"
                required
                minLength={6}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full rounded-lg border border-border bg-card px-3 py-2 text-ink outline-none focus:border-accent"
              />
            </div>
            <div>
              <label htmlFor="confirm" className="block text-sm text-ink-2 mb-1">Repetí la contraseña</label>
              <input
                id="confirm"
                type="password"
                required
                minLength={6}
                value={confirm}
                onChange={(e) => setConfirm(e.target.value)}
                className="w-full rounded-lg border border-border bg-card px-3 py-2 text-ink outline-none focus:border-accent"
              />
            </div>
            <button
              type="submit"
              disabled={loading}
              className="w-full rounded-full bg-accent text-white font-semibold py-2.5 hover:brightness-110 active:scale-[.98] transition disabled:opacity-60"
            >
              {loading ? "Guardando…" : "Guardar contraseña"}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
