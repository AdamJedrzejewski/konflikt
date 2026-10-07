import type { NextConfig } from "next";

// Adres backendu widziany z serwera strony, nie z przeglądarki.
// Lokalnie: uvicorn na porcie 8001. W kontenerach: http://backend:8000 (argument budowania).
const backendUrl = process.env.BACKEND_URL || "http://localhost:8001";

const nextConfig: NextConfig = {
  output: "standalone",
  async rewrites() {
    return [{ source: "/api/v1/:path*", destination: `${backendUrl}/api/v1/:path*` }];
  },
};

export default nextConfig;
