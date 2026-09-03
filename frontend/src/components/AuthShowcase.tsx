const VALUE_PROPS = [
  {
    icon: "🔍",
    title: "Autodiagnóstico en 10 minutos",
    text: "24 preguntas simples, sin jerga técnica, pensadas para alguien que no maneja tecnología.",
  },
  {
    icon: "📊",
    title: "Un puntaje claro",
    text: "Sabés de un vistazo en qué estás bien y dónde tu empresa está expuesta.",
  },
  {
    icon: "✅",
    title: "Plan de acción paso a paso",
    text: "Te decimos qué resolver primero y cómo hacerlo, explicado en criollo.",
  },
];

export default function AuthShowcase() {
  return (
    <div className="relative flex-1 flex flex-col justify-center px-8 py-12 lg:px-16 overflow-hidden">
      <div
        className="absolute -top-24 -left-24 w-96 h-96 rounded-full blur-3xl opacity-20"
        style={{ background: "var(--color-accent)" }}
        aria-hidden
      />

      <div className="relative flex items-center gap-3 mb-6">
        <svg width="40" height="40" viewBox="0 0 24 24" fill="none" aria-hidden>
          <path
            d="M12 2 4 5v6c0 5 3.4 8.7 8 9 4.6-.3 8-4 8-9V5l-8-3Z"
            fill="var(--color-accent)"
            fillOpacity="0.18"
            stroke="var(--color-accent)"
            strokeWidth="1.5"
          />
          <path
            d="M8.5 12.2 11 14.7 15.5 9.5"
            stroke="var(--color-accent)"
            strokeWidth="1.8"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </svg>
        <span className="text-2xl font-bold">CyberPyME</span>
      </div>

      <h1 className="relative text-3xl font-bold leading-tight mb-3 max-w-md">
        Sabé qué tan expuesta está tu empresa a un ciberataque
      </h1>
      <p className="relative text-ink-2 mb-10 max-w-md">
        Y qué hacer al respecto, paso a paso — pensado para PyMEs sin área de IT.
      </p>

      <div className="relative space-y-5 max-w-md">
        {VALUE_PROPS.map((v) => (
          <div key={v.title} className="flex gap-3">
            <span className="text-xl leading-none shrink-0 mt-0.5">{v.icon}</span>
            <div>
              <p className="font-semibold">{v.title}</p>
              <p className="text-sm text-ink-muted">{v.text}</p>
            </div>
          </div>
        ))}
      </div>

      <p className="relative text-xs text-ink-muted mt-10 max-w-md">
        Basado en estándares internacionales de ciberseguridad (NIST CSF 2.0 + CIS Controls v8.1).
      </p>
    </div>
  );
}
