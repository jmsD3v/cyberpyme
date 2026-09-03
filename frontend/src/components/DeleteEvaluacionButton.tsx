"use client";

export default function DeleteEvaluacionButton({ action }: { action: () => Promise<void> }) {
  return (
    <form
      action={action}
      onSubmit={(e) => {
        if (!confirm("¿Borrar esta evaluación? No se puede deshacer.")) {
          e.preventDefault();
        }
      }}
    >
      <button
        type="submit"
        className="text-sm text-status-critico hover:underline"
      >
        Borrar esta evaluación
      </button>
    </form>
  );
}
