CREATE TYPE user_role AS ENUM ('admin', 'accountant');

CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name VARCHAR(120) NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  role user_role NOT NULL DEFAULT 'accountant',
  is_active BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE invoices (
  id SERIAL PRIMARY KEY,
  uploaded_by INTEGER NOT NULL REFERENCES users(id),
  file_name VARCHAR(255) NOT NULL,
  file_path VARCHAR(500) NOT NULL,
  vendor_name VARCHAR(255),
  gstin VARCHAR(15),
  invoice_number VARCHAR(100),
  invoice_date DATE,
  hsn_sac_codes TEXT,
  taxable_amount DOUBLE PRECISION,
  cgst DOUBLE PRECISION,
  sgst DOUBLE PRECISION,
  igst DOUBLE PRECISION,
  grand_total DOUBLE PRECISION,
  status VARCHAR(20) NOT NULL DEFAULT 'pending',
  paid_at TIMESTAMPTZ,
  ocr_confidence DOUBLE PRECISION,
  gst_valid BOOLEAN NOT NULL DEFAULT FALSE,
  gst_calculation_correct BOOLEAN NOT NULL DEFAULT FALSE,
  duplicate_of_id INTEGER REFERENCES invoices(id),
  ai_correction_notes TEXT,
  raw_ocr_json JSONB,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE invoice_items (
  id SERIAL PRIMARY KEY,
  invoice_id INTEGER NOT NULL REFERENCES invoices(id) ON DELETE CASCADE,
  description VARCHAR(255),
  hsn_sac_code VARCHAR(30),
  quantity INTEGER,
  taxable_amount DOUBLE PRECISION,
  cgst DOUBLE PRECISION,
  sgst DOUBLE PRECISION,
  igst DOUBLE PRECISION,
  total_amount DOUBLE PRECISION
);

CREATE TABLE audit_logs (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  action VARCHAR(120) NOT NULL,
  entity VARCHAR(120) NOT NULL,
  entity_id VARCHAR(120),
  details TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
