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
        <div className="max-w-4xl mx-auto px-6 py-4 flex items-center justify-between">
          <Link href="/" className="font-bold text-lg">
            CyberPyME{empresa ? <span className="text-ink-muted font-normal"> — {empresa}</span> : null}
          </Link>
          <form action={logout}>
            <button type="submit" className="text-sm text-ink-muted hover:text-ink transition">
              Salir
            </button>
          </form>
        </div>
      </header>
      <main className="flex-1 max-w-4xl w-full mx-auto px-6 py-8">{children}</main>
    </div>
  );
}
