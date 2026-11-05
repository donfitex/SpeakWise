# syntax=docker/dockerfile:1
FROM node:24-bookworm-slim AS build
WORKDIR /app
COPY frontend/package*.json ./
RUN --mount=type=secret,id=system_ca,required=true NODE_EXTRA_CA_CERTS=/run/secrets/system_ca npm ci
COPY frontend/ ./
RUN npm run build
FROM caddy:2-alpine
COPY --from=build /app/dist /srv
COPY deploy/Caddyfile /etc/caddy/Caddyfile
