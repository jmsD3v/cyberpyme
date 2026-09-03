import { describe, it, expect } from "vitest";
import { render } from "@testing-library/react";
import EvolucionChart from "./EvolucionChart";
import { RISK_COLOR } from "@/lib/types";

const puntos = [
  { fecha: "2026-06-05", score: 30, risk_level: "CRITICO" as const },
  { fecha: "2026-07-05", score: 45, risk_level: "ALTO" as const },
  { fecha: "2026-08-04", score: 62, risk_level: "MEDIO" as const },
  { fecha: "2026-09-03", score: 85, risk_level: "BAJO" as const },
];

describe("EvolucionChart", () => {
  it("dibuja un punto (circulo) por cada evaluacion", () => {
    const { container } = render(<EvolucionChart puntos={puntos} />);
    const circulos = container.querySelectorAll("circle");
    expect(circulos).toHaveLength(puntos.length);
  });

  it("colorea cada punto segun su nivel de riesgo", () => {
    const { container } = render(<EvolucionChart puntos={puntos} />);
    const circulos = container.querySelectorAll("circle");
    puntos.forEach((p, i) => {
      expect(circulos[i]).toHaveAttribute("fill", RISK_COLOR[p.risk_level]);
    });
  });

  it("el ultimo punto queda mas alto que el primero cuando el score mejora", () => {
    const { container } = render(<EvolucionChart puntos={puntos} />);
    const circulos = container.querySelectorAll("circle");
    const yPrimero = Number(circulos[0].getAttribute("cy"));
    const yUltimo = Number(circulos[circulos.length - 1].getAttribute("cy"));
    // Score mas alto = mas arriba = menor "y" (el SVG crece hacia abajo).
    expect(yUltimo).toBeLessThan(yPrimero);
  });

  it("no rompe con un solo punto", () => {
    const { container } = render(
      <EvolucionChart puntos={[{ fecha: "2026-09-03", score: 50, risk_level: "MEDIO" }]} />
    );
    expect(container.querySelectorAll("circle")).toHaveLength(1);
  });
});
