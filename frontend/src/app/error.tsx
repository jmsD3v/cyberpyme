"use client";

export default function Error({ reset }: { error: Error & { digest?: string }; reset: () => void }) {
  return (
    <div className="flex-1 flex items-center justify-center p-6 text-center">
      <div className="max-w-sm">
        <div className="text-4xl mb-3">⚠️</div>
        <h1 className="text-xl font-bold mb-2">Algo salió mal</h1>
        <p className="text-ink-2 text-sm mb-6">
          Hubo un problema inesperado. Probá de nuevo en un momento.
        </p>
        <button
          type="button"
          onClick={reset}
          className="rounded-full bg-accent text-white text-sm font-semibold px-5 py-2.5 hover:brightness-110 active:scale-[.98] transition"
        >
          Reintentar
        </button>
      </div>
    </div>
  );
}
