import { type NextRequest } from "next/server";
import { updateSession } from "@/lib/supabase/middleware";

// Next.js 16: "middleware" se renombro a "proxy" (mismo comportamiento,
// solo cambia el nombre del archivo/funcion). La proteccion real de datos
// vive en RLS (Supabase) -- esto es solo UX (redirigir a /login).
export function proxy(request: NextRequest) {
  return updateSession(request);
}

export const config = {
  matcher: [
    "/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)",
  ],
};
