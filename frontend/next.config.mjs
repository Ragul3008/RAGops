/** @type {import('next').NextConfig} */
const config = {
  experimental: { typedRoutes: true },
  images: {
    domains: ["storage.ragops.io"],
  },
  async headers() {
    return [{
      source: "/(.*)",
      headers: [
        { key: "X-Frame-Options",         value: "DENY" },
        { key: "X-Content-Type-Options",   value: "nosniff" },
        { key: "X-XSS-Protection",         value: "1; mode=block" },
        { key: "Referrer-Policy",          value: "strict-origin" },
        { key: "Permissions-Policy",       value: "camera=(), microphone=()" },
      ],
    }];
  },
};

export default config;
