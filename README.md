# InvoxelAI GST/Bill OCR Web Application

Production-style full-stack GST invoice OCR platform with FastAPI + Next.js.

## Tech Stack
- Backend: FastAPI, SQLAlchemy (async), JWT auth
- Frontend: Next.js 15, TypeScript, Tailwind CSS, shadcn-style components
- Database: PostgreSQL
- OCR: PaddleOCR (primary), EasyOCR (fallback)
- PDF/Image Processing: OpenCV, pdfplumber, PyMuPDF
- Charts: Recharts
- DevOps: Docker, Docker Compose

## Features
- Upload `PDF/JPG/PNG` invoices
- OCR extraction for vendor, GSTIN, invoice no/date, HSN/SAC, tax amounts, grand total
- GSTIN format validation
- GST arithmetic mismatch detection
- AI-based correction heuristics for weak/missing fields
- Duplicate invoice detection
- Role-based auth (`admin`, `accountant`)
- Audit logs
- Dashboard KPIs + monthly GST charts
- Search/filter + pagination
- Export CSV/Excel/JSON
- Chat-like query (`Show invoices where GST > 5000`)
- Dark/light theme and mobile-responsive UI
- OCR confidence visibility

## Quick Start (Docker)
```bash
docker compose up --build
```

Then seed realistic demo data:
```bash
docker compose exec backend python /scripts/seed_data.py
```

Access:
- Frontend: `http://localhost:3000`
- Backend: `http://localhost:8000`
- Swagger: `http://localhost:8000/docs`

Demo users:
- Admin: `admin@invoxel.ai` / `Admin@1234`
- Accountant: `accountant@invoxel.ai` / `Accountant@1234`

## Local Setup (Without Docker)

### 1) Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python -m app.create_tables
uvicorn app.main:app --reload
```

### 2) Frontend
```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

## API Overview
Detailed endpoint docs: [`docs/API_DOCUMENTATION.md`](docs/API_DOCUMENTATION.md)

## Database
SQL schema: [`docs/database_schema.sql`](docs/database_schema.sql)

## Tests
```bash
cd backend
pytest
```

## 10 Realistic Sample Invoices
- Metadata seed set: [`sample_data/invoices.json`](sample_data/invoices.json)
- OCR/parser text fixtures: `sample_data/mock_invoice_texts/inv_01.txt` ... `inv_10.txt`

These are used by `scripts/seed_data.py` to populate PostgreSQL with realistic invoice and invoice item data.

## Project Structure
See [`docs/FOLDER_STRUCTURE.md`](docs/FOLDER_STRUCTURE.md).

## Deployment Notes
See [`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md).

## Internship/Open Source Readiness
- Modular backend architecture
- Type-safe frontend modules
- Role-based access controls
- Validation + auditability
- Export/reporting support
- Seed/test support for quick onboarding

## Resume Bullet (Suggested)
Built a production-style AI-powered GST invoice OCR platform using FastAPI, PaddleOCR, Next.js 15, and PostgreSQL with JWT RBAC, analytics dashboards, export pipelines, and Dockerized deployment.
