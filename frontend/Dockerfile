# Strona OBSIL (Next.js, tryb produkcyjny). Budowanie z katalogu frontend/.
FROM node:22-alpine AS build
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
# Adres backendu wewnątrz sieci kontenerów; wpisywany do konfiguracji przy budowaniu.
ARG BACKEND_URL=http://backend:8000
ENV BACKEND_URL=${BACKEND_URL} NEXT_TELEMETRY_DISABLED=1
RUN npm run build

FROM node:22-alpine
WORKDIR /app
ENV NODE_ENV=production NEXT_TELEMETRY_DISABLED=1 HOSTNAME=0.0.0.0 PORT=3000
COPY --from=build /app/.next/standalone ./
COPY --from=build /app/.next/static ./.next/static
COPY --from=build /app/public ./public
USER node
EXPOSE 3000
CMD ["node", "server.js"]
