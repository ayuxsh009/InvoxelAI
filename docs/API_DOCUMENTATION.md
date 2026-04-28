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
- `GET /invoices?q=&status=&gst_valid=&duplicate_only=&start_date=&end_date=&month=&year=&min_gst=&max_gst=&page=&page_size=`
- `GET /invoices/{invoice_id}`
- `PATCH /invoices/{invoice_id}/status`
  - body:
    ```json
    { "status": "paid", "paid_at": "2026-05-01T10:00:00Z" }
    ```

## Analytics
- `GET /analytics/dashboard`

## Exports
- `GET /exports/csv?q=&status=&gst_valid=&duplicate_only=&start_date=&end_date=&month=&year=&min_gst=&max_gst=`
- `GET /exports/excel?q=&status=&gst_valid=&duplicate_only=&start_date=&end_date=&month=&year=&min_gst=&max_gst=`
- `GET /exports/json?q=&status=&gst_valid=&duplicate_only=&start_date=&end_date=&month=&year=&min_gst=&max_gst=`

## Chat
- `POST /chat/query`
  - body:
    ```json
    { "message": "Show invoices where GST > 5000" }
    ```

## Audit Logs (Admin)
- `GET /audit-logs?action=&entity=&user_id=&q=&start_date=&end_date=&page=&page_size=`
