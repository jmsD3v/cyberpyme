/** Traduce mensajes de error de Supabase Auth (en inglés, técnicos) a algo
 * que un dueño de PyME sin conocimientos de IT pueda entender. Los mensajes
 * de Supabase no están pensados para mostrarse tal cual a un usuario final. */
const KNOWN_ERRORS: [match: string, translated: string][] = [
  ["Invalid login credentials", "El email o la contraseña no son correctos."],
  ["Email not confirmed", "Todavía no confirmaste tu email — revisá tu casilla de entrada (y la carpeta de spam)."],
  ["User already registered", "Ya existe una cuenta con ese email. Iniciá sesión en vez de crear una nueva."],
  ["Password should be at least", "La contraseña tiene que tener al menos 6 caracteres."],
  ["rate limit exceeded", "Se hicieron demasiados intentos en poco tiempo. Esperá unos minutos y probá de nuevo."],
  ["you can only request this after", "Se hicieron demasiados intentos en poco tiempo. Esperá un momento y probá de nuevo."],
  ["Unable to validate email address", "Ese email no parece válido — revisalo."],
];

export function translateAuthError(message: string): string {
  const found = KNOWN_ERRORS.find(([match]) => message.toLowerCase().includes(match.toLowerCase()));
  return found?.[1] ?? "Ocurrió un problema al procesar la solicitud. Probá de nuevo en unos minutos.";
}
