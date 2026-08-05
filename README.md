# Luminance

Aplicación web que extrae paletas de colores dominantes de imágenes usando clustering perceptual (K-Means en espacio LAB).

Subís una foto — un fotograma de película, un paisaje, un cuadro — y el sistema devuelve los colores dominantes ordenados, con sus valores hex y porcentaje de presencia.

## Stack

| Capa | Tecnología |
|---|---|
| Frontend | Next.js 16 (App Router) + TypeScript + Tailwind CSS 4 |
| Auth | Clerk |
| Base de datos | PostgreSQL via NeonDB + Prisma ORM |
| Procesamiento | Python (FastAPI + OpenCV + scikit-learn) |
| Deploy | Vercel (frontend) + Render/Railway (microservicio) |

## Estructura del proyecto

```
luminance-app/
  /web    → Frontend Next.js
  /api    → Microservicio FastAPI
```

## Correr en local

### Frontend (`/web`)

```bash
cd web
pnpm install
cp .env.example .env.local   # completar con tus claves
pnpm dev
```

Abre [http://localhost:3000](http://localhost:3000).

### Microservicio Python (`/api`)

```bash
cd api
uv venv
uv pip install -r requirements.txt
cp .env.example .env         # completar con tus claves
uv run uvicorn main:app --reload
```

Abre [http://localhost:8000/health](http://localhost:8000/health) — debería devolver `{"status": "ok"}`.

## Variables de entorno

Ver `.env.example` en cada subdirectorio para la lista completa de variables necesarias.