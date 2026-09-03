import Link from "next/link";

export const metadata = { title: "Política de privacidad — CyberPyME" };

export default function PrivacidadPage() {
  return (
    <div className="flex-1 max-w-2xl w-full mx-auto px-6 py-12">
      <Link href="/login" className="text-sm text-accent hover:underline">
        ← Volver
      </Link>
      <h1 className="text-2xl font-bold mt-4 mb-2">Política de privacidad</h1>
      <p className="text-ink-muted text-sm mb-8">Última actualización: septiembre de 2026</p>

      <div className="space-y-6 text-ink-2 leading-relaxed">
        <section>
          <h2 className="font-semibold text-ink mb-2">Qué datos recolectamos</h2>
          <ul className="list-disc pl-5 space-y-1">
            <li>Tu email y contraseña, para el login (la contraseña nunca la vemos en texto plano — la maneja Supabase, nuestro proveedor de autenticación).</li>
            <li>El nombre de tu empresa.</li>
            <li>Las respuestas que cargás en cada autodiagnóstico, y el puntaje/resultado calculado.</li>
          </ul>
        </section>

        <section>
          <h2 className="font-semibold text-ink mb-2">Para qué los usamos</h2>
          <p>
            Únicamente para darte el servicio: calcular tu puntaje, guardar el
            historial de tus evaluaciones y mostrarte tu guía de acciones. No vendemos
            ni compartimos tus datos con terceros para publicidad ni ningún otro fin
            comercial.
          </p>
        </section>

        <section>
          <h2 className="font-semibold text-ink mb-2">Dónde se guardan</h2>
          <p>
            Tus datos viven en Supabase (base de datos con seguridad a nivel de fila:
            cada empresa solo puede ver sus propios datos, nunca los de otra). El
            cálculo del puntaje corre en un servicio separado que no guarda nada — solo
            recibe las respuestas, calcula, y responde.
          </p>
        </section>

        <section>
          <h2 className="font-semibold text-ink mb-2">Tus derechos</h2>
          <p>
            Podés acceder, corregir o borrar tus datos en cualquier momento — el nombre
            de tu empresa desde{" "}
            <Link href="/cuenta" className="text-accent hover:underline">
              tu cuenta
            </Link>
            , una evaluación puntual desde su detalle, o tu cuenta completa
            escribiéndonos. Esto está en línea con lo que establece la Ley 25.326 de
            Protección de Datos Personales de Argentina.
          </p>
        </section>

        <section>
          <h2 className="font-semibold text-ink mb-2">Contacto</h2>
          <p>
            Para cualquier consulta sobre tus datos, escribinos a{" "}
            <a href="mailto:contacto@jmsilva.dev" className="text-accent hover:underline">
              contacto@jmsilva.dev
            </a>
            .
          </p>
        </section>
      </div>
    </div>
  );
}
