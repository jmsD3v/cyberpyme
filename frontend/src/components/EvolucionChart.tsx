import { RISK_COLOR, type RiskLevel } from "@/lib/types";

interface Punto {
  fecha: string;
  score: number;
  risk_level: RiskLevel;
}

const WIDTH = 600;
const HEIGHT = 180;
const PAD_X = 24;
const PAD_TOP = 16;
const PAD_BOTTOM = 28;

export default function EvolucionChart({ puntos }: { puntos: Punto[] }) {
  const plotWidth = WIDTH - PAD_X * 2;
  const plotHeight = HEIGHT - PAD_TOP - PAD_BOTTOM;

  const xFor = (i: number) =>
    puntos.length === 1 ? PAD_X + plotWidth / 2 : PAD_X + (i / (puntos.length - 1)) * plotWidth;
  const yFor = (score: number) => PAD_TOP + (1 - score / 100) * plotHeight;

  const linePath = puntos.map((p, i) => `${i === 0 ? "M" : "L"} ${xFor(i)} ${yFor(p.score)}`).join(" ");
  const areaPath = `${linePath} L ${xFor(puntos.length - 1)} ${PAD_TOP + plotHeight} L ${xFor(0)} ${PAD_TOP + plotHeight} Z`;

  return (
    <svg viewBox={`0 0 ${WIDTH} ${HEIGHT}`} width="100%" height={HEIGHT} role="img" aria-label="Evolución del score a lo largo del tiempo">
      {[0, 25, 50, 75, 100].map((v) => (
        <line
          key={v}
          x1={PAD_X}
          x2={WIDTH - PAD_X}
          y1={yFor(v)}
          y2={yFor(v)}
          stroke="var(--color-border)"
          strokeWidth="1"
        />
      ))}

      <path d={areaPath} fill="var(--color-accent)" fillOpacity="0.08" stroke="none" />
      <path d={linePath} fill="none" stroke="var(--color-accent)" strokeWidth="2" strokeLinejoin="round" strokeLinecap="round" />

      {puntos.map((p, i) => (
        <circle
          key={i}
          cx={xFor(i)}
          cy={yFor(p.score)}
          r="5"
          fill={RISK_COLOR[p.risk_level]}
          stroke="var(--color-surface)"
          strokeWidth="2"
        />
      ))}

      {puntos.map((p, i) => {
        if (puntos.length > 6 && i % Math.ceil(puntos.length / 6) !== 0 && i !== puntos.length - 1) return null;
        return (
          <text
            key={i}
            x={xFor(i)}
            y={HEIGHT - 8}
            textAnchor="middle"
            fontSize="10"
            fill="var(--color-ink-muted)"
          >
            {new Date(p.fecha).toLocaleDateString("es-AR", { day: "2-digit", month: "2-digit" })}
          </text>
        );
      })}
    </svg>
  );
}
