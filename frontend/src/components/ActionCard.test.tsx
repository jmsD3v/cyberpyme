import { describe, it, expect } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import ActionCard from "./ActionCard";
import type { Action, Question } from "@/lib/types";

const action: Action = {
  title: "Activar MFA en correo, banca y servicios críticos",
  domain: "accesos",
  priority: "P1",
  impact: "MUY_ALTO",
  effort: "BAJO",
  time: "1-3 días",
  why: "Una contraseña filtrada ya no alcanza si además hace falta un segundo paso.",
  steps: ["Activar la verificación en dos pasos en el correo.", "Repetir en el homebanking."],
  question_id: "ACC-02",
  risk: "credential_compromise",
};

const question: Question = {
  id: "ACC-02",
  domain: "accesos",
  question: "¿Las cuentas críticas tienen MFA activado?",
  weight: 1,
  risk: "credential_compromise",
  nist: ["PR.AA"],
  cis: ["6"],
  recommendation_id: "REC-ACC-02",
  help: "",
};

describe("ActionCard", () => {
  it("muestra el titulo y la prioridad, colapsada por defecto (clase 'hidden' + 'print:block')", () => {
    render(<ActionCard action={action} question={question} domainLabel="Accesos" index={0} />);
    expect(screen.getByText(action.title)).toBeInTheDocument();
    expect(screen.getByText("Urgente")).toBeInTheDocument();
    // El contenido esta siempre en el DOM (para que el PDF pueda forzarlo
    // visible con print:block), oculto en pantalla via la clase "hidden".
    expect(screen.getByText(action.why).closest("div")).toHaveClass("hidden", "print:block");
  });

  it("se expande al hacer click: saca la clase 'hidden' y el porque/pasos quedan visibles", () => {
    render(<ActionCard action={action} question={question} domainLabel="Accesos" index={0} />);
    fireEvent.click(screen.getByRole("button"));
    expect(screen.getByText(action.why).closest("div")).not.toHaveClass("hidden");
    for (const step of action.steps) {
      expect(screen.getByText(step)).toBeInTheDocument();
    }
  });

  it("se puede volver a colapsar", () => {
    render(<ActionCard action={action} question={question} domainLabel="Accesos" index={0} />);
    const boton = screen.getByRole("button");
    fireEvent.click(boton);
    expect(screen.getByText(action.why).closest("div")).not.toHaveClass("hidden");
    fireEvent.click(boton);
    expect(screen.getByText(action.why).closest("div")).toHaveClass("hidden");
  });

  it("muestra la traza a NIST/CIS de la pregunta de origen", () => {
    render(<ActionCard action={action} question={question} domainLabel="Accesos" index={0} />);
    fireEvent.click(screen.getByRole("button"));
    expect(screen.getByText(/PR\.AA/)).toBeInTheDocument();
  });
});
