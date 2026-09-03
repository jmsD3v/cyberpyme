import type { MetadataRoute } from "next";

export default function manifest(): MetadataRoute.Manifest {
  return {
    name: "CyberPyME — Autodiagnóstico de ciberseguridad",
    short_name: "CyberPyME",
    description: "Autodiagnóstico de ciberseguridad para PyMEs sin área de IT",
    start_url: "/",
    display: "standalone",
    background_color: "#1e1e1e",
    theme_color: "#1e1e1e",
    icons: [
      {
        src: "/icon.svg",
        sizes: "any",
        type: "image/svg+xml",
      },
    ],
  };
}
