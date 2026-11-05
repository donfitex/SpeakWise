# syntax=docker/dockerfile:1
FROM node:24-bookworm-slim
WORKDIR /app
COPY package*.json ./
RUN --mount=type=secret,id=system_ca,required=true NODE_EXTRA_CA_CERTS=/run/secrets/system_ca npm install --package-lock=false
COPY . .
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
