# Deployment Guide

## Docker (Recommended)
1. Ensure Docker and Docker Compose are installed.
2. Run:
   ```bash
   docker compose up --build
   ```
3. Services:
   - Frontend: `http://localhost:3000`
   - Backend: `http://localhost:8000`
   - Swagger: `http://localhost:8000/docs`

## Seed Data
After containers are up:
```bash
docker compose exec backend python /scripts/seed_data.py
```

## Local Deployment Notes
- Configure `backend/.env` from `.env.example`.
- Use managed PostgreSQL in production.
- Set strong `SECRET_KEY` and tight CORS origins.
- Run behind reverse proxy (Nginx/Traefik) with TLS.
