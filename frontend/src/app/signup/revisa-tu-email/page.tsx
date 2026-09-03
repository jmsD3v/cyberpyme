import Link from "next/link";

export default function RevisaTuEmailPage() {
  return (
    <div className="flex-1 flex items-center justify-center p-6 text-center">
      <div className="max-w-sm">
        <div className="text-4xl mb-3">📬</div>
        <h1 className="text-xl font-bold mb-2">Revisá tu email</h1>
        <p className="text-ink-2 text-sm">
          Te mandamos un link de confirmación. Una vez que confirmes, iniciá
          sesión y vas a poder terminar de registrar tu empresa.
        </p>
        <Link href="/login" className="inline-block mt-6 text-accent hover:underline text-sm">
          Volver a iniciar sesión
        </Link>
      </div>
    </div>
  );
}
