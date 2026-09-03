import Link from "next/link";
import { logout } from "@/app/logout/actions";

export default function AppShell({
  empresa,
  children,
}: {
  empresa?: string;
  children: React.ReactNode;
}) {
  return (
    <div className="flex-1 flex flex-col">
      <header className="border-b border-border">
        <div className="max-w-4xl mx-auto px-6 py-4 flex flex-wrap items-center justify-between gap-x-4 gap-y-2">
          <Link href="/" className="font-bold text-lg">
            CyberPyME{empresa ? <span className="text-ink-muted font-normal"> — {empresa}</span> : null}
          </Link>
          <div className="flex items-center gap-5 shrink-0 no-print">
            <Link href="/guia-hardening" className="text-sm text-ink-muted hover:text-ink transition">
              Guía de hardening
            </Link>
            <Link href="/cuenta" className="text-sm text-ink-muted hover:text-ink transition">
              Cuenta
            </Link>
            <form action={logout}>
              <button type="submit" className="text-sm text-ink-muted hover:text-ink transition">
                Salir
              </button>
            </form>
          </div>
        </div>
      </header>
      <main className="flex-1 max-w-4xl w-full mx-auto px-6 py-8">{children}</main>
    </div>
  );
}
