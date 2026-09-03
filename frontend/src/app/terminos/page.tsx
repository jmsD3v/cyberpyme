import Link from "next/link";

export const metadata = { title: "Términos de servicio — CyberPyME" };

export default function TerminosPage() {
  return (
    <div className="flex-1 max-w-2xl w-full mx-auto px-6 py-12">
      <Link href="/login" className="text-sm text-accent hover:underline">
        ← Volver
      </Link>
      <h1 className="text-2xl font-bold mt-4 mb-2">Términos de servicio</h1>
      <p className="text-ink-muted text-sm mb-8">Última actualización: septiembre de 2026</p>

      <div className="space-y-6 text-ink-2 leading-relaxed">
        <section>
          <h2 className="font-semibold text-ink mb-2">Qué es CyberPyME</h2>
          <p>
            CyberPyME es una herramienta de autodiagnóstico de ciberseguridad pensada
            para PyMEs sin área de IT. Respondés un cuestionario y te devolvemos un
            puntaje, un nivel de riesgo por dominio y una guía de acciones priorizadas
            para mejorar, basada en la metodología NIST CSF 2.0 y CIS Controls v8.1
            (nivel IG1).
          </p>
        </section>

        <section>
          <h2 className="font-semibold text-ink mb-2">Es un punto de partida, no una garantía</h2>
          <p>
            El resultado depende enteramente de las respuestas que cargues — no
            verificamos ni auditamos tu infraestructura real. Un puntaje alto no
            garantiza que tu empresa esté libre de riesgos, y CyberPyME no reemplaza
            una auditoría de seguridad profesional. Lo usás como guía orientativa, bajo
            tu propia responsabilidad.
          </p>
        </section>

        <section>
          <h2 className="font-semibold text-ink mb-2">Tu cuenta y tus datos</h2>
          <p>
            Cada cuenta representa una empresa. Sos responsable de la información que
            cargues y de mantener tu contraseña segura. Podés borrar evaluaciones
            individuales vos mismo desde el detalle de cada una. Si querés dar de baja
            tu cuenta por completo, escribinos y lo hacemos.
          </p>
        </section>

        <section>
          <h2 className="font-semibold text-ink mb-2">Disponibilidad</h2>
          <p>
            Este es un proyecto en desarrollo activo — puede haber interrupciones,
            cambios de funcionalidad o mantenimiento sin aviso previo. No garantizamos
            disponibilidad continua del servicio.
          </p>
        </section>

        <section>
          <h2 className="font-semibold text-ink mb-2">Límite de responsabilidad</h2>
          <p>
            CyberPyME se ofrece &ldquo;tal cual&rdquo;, sin garantías de ningún tipo. No nos
            hacemos responsables por decisiones tomadas en base a los resultados del
            autodiagnóstico, ni por incidentes de seguridad que puedan ocurrir en tu
            empresa independientemente de haber usado esta herramienta.
          </p>
        </section>

        <section>
          <h2 className="font-semibold text-ink mb-2">Contacto</h2>
          <p>
            Para consultas sobre estos términos, escribinos a{" "}
            <a href="mailto:juanmanuelsilva06@gmail.com" className="text-accent hover:underline">
              juanmanuelsilva06@gmail.com
            </a>
            .
          </p>
        </section>
      </div>
    </div>
  );
}
