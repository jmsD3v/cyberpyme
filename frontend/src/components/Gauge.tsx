"use client";

import { useEffect, useState } from "react";
import { RISK_COLOR, RISK_LABEL, type RiskLevel } from "@/lib/types";

export default function Gauge({ score, riskLevel }: { score: number; riskLevel: RiskLevel }) {
  const [display, setDisplay] = useState(0);
  const r = 68;
  const circumference = 2 * Math.PI * r;
  const target = circumference * (1 - Math.max(0, Math.min(100, score)) / 100);
  const color = RISK_COLOR[riskLevel];

  useEffect(() => {
    const start = performance.now();
    const duration = 900;
    let raf: number;
    function step(now: number) {
      const t = Math.min(1, (now - start) / duration);
      const eased = 1 - Math.pow(1 - t, 3);
      setDisplay(Math.round(score * eased));
      if (t < 1) raf = requestAnimationFrame(step);
    }
    raf = requestAnimationFrame(step);
    return () => cancelAnimationFrame(raf);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [score]);

  return (
    <div className="relative inline-block">
      <div
        className="absolute inset-[10%] rounded-full blur-2xl opacity-35"
        style={{ background: color }}
      />
      <svg viewBox="0 0 160 160" width={160} height={160} className="relative">
        <circle cx="80" cy="80" r={r} fill="none" stroke="var(--color-track)" strokeWidth="14" />
        <circle
          cx="80"
          cy="80"
          r={r}
          fill="none"
          stroke={color}
          strokeWidth="14"
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={target}
          transform="rotate(-90 80 80)"
          style={{ transition: "stroke-dashoffset 1s cubic-bezier(.22,1,.36,1)" }}
        />
        <text x="80" y="76" textAnchor="middle" fontSize="30" fontWeight="700" fill="var(--color-ink)">
          {display}
        </text>
        <text x="80" y="98" textAnchor="middle" fontSize="11" fill="var(--color-ink-muted)">
          /100
        </text>
      </svg>
      <p className="text-center mt-1">
        <span
          className="text-xs font-bold text-white px-3 py-1 rounded-full"
          style={{ background: color }}
        >
          Riesgo {RISK_LABEL[riskLevel]}
        </span>
      </p>
    </div>
  );
}
