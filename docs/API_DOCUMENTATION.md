# API Documentation

Base URL: `http://localhost:8000/api/v1`
Swagger: `http://localhost:8000/docs`

## Auth
- `POST /auth/register`
- `POST /auth/login`
- `GET /auth/me`

## Users
- `GET /users/profile`

## Invoices
- `POST /invoices/upload` (multipart: `file`)
- `GET /invoices?q=&month=&year=&min_gst=&max_gst=&page=&page_size=`
- `GET /invoices/{invoice_id}`

## Analytics
- `GET /analytics/dashboard`

## Exports
- `GET /exports/csv`
- `GET /exports/excel`
- `GET /exports/json`

## Chat
- `POST /chat/query`
  - body:
    ```json
    { "message": "Show invoices where GST > 5000" }
    ```

## Audit Logs (Admin)
- `GET /audit-logs`
