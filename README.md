# Project 5: AWS EKS Observability Dashboard

Aplicación dividida en:
- `app/api`: backend FastAPI
- `app/web`: frontend Next.js + Tailwind

## Arquitectura actual
- El frontend se sirve en `/`
- Las llamadas a `/api/*` se enrutan desde Next.js hacia FastAPI (path-based routing)
- Esto permite usar un solo host y evita problemas de CORS en el navegador

## Backend (`app/api`)
### Endpoints
- `GET /` -> redirect a `/docs`
- `GET /api/health` -> `{ "status": "ok" }`
- `GET /api/status` -> `{ "up": true, "latency_ms": number }`
- `GET /api/version` -> `{ "commit": str, "build_time": str, "environment": str }`

Variables de entorno para version:
- `COMMIT_SHA` (default: `unknown`)
- `BUILD_TIME` (default: `unknown`)
- `ENVIRONMENT` (default: `dev`)

### Ejecutar backend en local
```bash
cd app/api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Ejecutar backend con Docker
```bash
cd app/api
docker build -t observability-api:latest .
docker run -d --name observability-api \
  -p 8000:8000 \
  -e COMMIT_SHA="local" \
  -e BUILD_TIME="$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  -e ENVIRONMENT="dev" \
  observability-api:latest
```

> Nota: en despliegue conjunto con frontend usa `docker-compose.yml` desde la raíz del proyecto.

## Frontend (`app/web`)
El frontend hace polling cada 5 segundos de:
- `/api/status`
- `/api/version`

Muestra:
- Status (UP/DOWN)
- Latency
- Commit SHA
- Build time

### Path-based routing configurado en Next.js
En `app/web/next.config.js`:
- `/api/:path*` -> `${BACKEND_URL}/api/:path*`

Si no defines `BACKEND_URL`, usa por defecto:
- `http://127.0.0.1:8000`

### Ejecutar frontend en local
```bash
cd app/web
npm install
BACKEND_URL="http://127.0.0.1:8000" npm run dev
```

Abre:
- `http://localhost:3000`

## Despliegue recomendado (mismo host)
Objetivo:
- `https://tu-host/` -> Next.js
- `https://tu-host/api/*` -> FastAPI (mediante rewrite de Next.js)

### Opción recomendada: Docker Compose (front + back)
Desde la raíz `project5-aws-eks-observability-dashboard`:

```bash
docker compose up --build -d
```

Esto levanta:
- `web` en `http://localhost:3000`
- `api` en red interna de Docker (`api:8000`)

El frontend enruta:
- `/api/*` -> `http://api:8000/api/*` (mismo host para navegador, sin CORS)

Importante:
- En Next.js este rewrite se resuelve en build.
- `docker-compose.yml` ya pasa `BACKEND_URL=http://api:8000` como `build.args` para que quede correcto dentro de la imagen.

Validación rápida:
```bash
curl http://localhost:3000/api/health
curl http://localhost:3000/api/version
curl http://localhost:3000/api/status
```

Para detener:
```bash
docker compose down
```

### Opción manual (sin compose)
1. Desplegar backend FastAPI (contenedor o proceso) escuchando en `8000`.
2. Desplegar frontend Next.js.
3. Configurar `BACKEND_URL` en frontend apuntando al backend accesible desde el runtime de Next.js (por ejemplo `http://127.0.0.1:8000`).
4. Publicar solo el frontend en el host público; el navegador consumirá `/api/*` en el mismo dominio.

## Nota de diseño
“Elegí path-based routing para simplificar CORS, TLS y operación. Si necesitara más aislamiento o políticas distintas, migraría a subdominios.”
