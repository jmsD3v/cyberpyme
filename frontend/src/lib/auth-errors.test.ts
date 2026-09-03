import { describe, it, expect } from "vitest";
import { translateAuthError } from "./auth-errors";

describe("translateAuthError", () => {
  it("traduce credenciales invalidas", () => {
    expect(translateAuthError("Invalid login credentials")).toBe(
      "El email o la contraseña no son correctos."
    );
  });

  it("traduce email no confirmado", () => {
    expect(translateAuthError("Email not confirmed")).toContain("confirmaste tu email");
  });

  it("traduce usuario ya registrado", () => {
    expect(translateAuthError("User already registered")).toContain("Ya existe una cuenta");
  });

  it("es insensible a mayusculas/minusculas", () => {
    expect(translateAuthError("invalid login credentials")).toBe(
      "El email o la contraseña no son correctos."
    );
  });

  it("matchea por substring, no exacto", () => {
    expect(translateAuthError("AuthApiError: Invalid login credentials (400)")).toBe(
      "El email o la contraseña no son correctos."
    );
  });

  it("cae al mensaje generico para errores desconocidos", () => {
    expect(translateAuthError("some completely unmapped error")).toBe(
      "Ocurrió un problema al procesar la solicitud. Probá de nuevo en unos minutos."
    );
  });

  it("nunca devuelve el texto crudo en ingles", () => {
    const casos = [
      "Invalid login credentials",
      "Email not confirmed",
      "User already registered",
      "Password should be at least 6 characters",
      "email rate limit exceeded",
      "you can only request this after 42 seconds",
      "Unable to validate email address: invalid format",
    ];
    for (const caso of casos) {
      const resultado = translateAuthError(caso);
      expect(resultado).not.toBe(caso);
      expect(resultado).toMatch(/[áéíóúñ]/i);
    }
  });
});
