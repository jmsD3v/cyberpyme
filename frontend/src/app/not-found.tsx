import Link from "next/link";

export default function NotFound() {
  return (
    <div className="flex-1 flex items-center justify-center p-6 text-center">
      <div className="max-w-sm">
        <div className="text-4xl mb-3">🔍</div>
        <h1 className="text-xl font-bold mb-2">Esta página no existe</h1>
        <p className="text-ink-2 text-sm mb-6">
          Revisá el link o volvé al inicio.
        </p>
        <Link
          href="/"
          className="inline-block rounded-full bg-accent text-white text-sm font-semibold px-5 py-2.5 hover:brightness-110 active:scale-[.98] transition"
        >
          Volver al inicio
        </Link>
      </div>
    </div>
  );
}
