-- =============================================================================
-- SANSON Legal OS — PostgreSQL Production Schema
-- =============================================================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- -----------------------------------------------------------------------------
-- ENUMS
-- -----------------------------------------------------------------------------

CREATE TYPE user_role AS ENUM ('client', 'lawyer', 'paralegal', 'admin');
CREATE TYPE case_category AS ENUM (
  'criminal', 'civil', 'labor', 'family', 'cybercrime', 'administrative', 'other'
);
CREATE TYPE case_priority AS ENUM ('low', 'medium', 'high', 'urgent');
CREATE TYPE payment_status AS ENUM ('pending', 'processing', 'completed', 'failed', 'refunded');
CREATE TYPE task_status AS ENUM ('pending', 'in_progress', 'completed', 'cancelled');
CREATE TYPE notification_type AS ENUM (
  'case_update', 'document_upload', 'assignment', 'ai_complete',
  'message', 'payment', 'system', 'reminder'
);

-- -----------------------------------------------------------------------------
-- ROLES & PERMISSIONS
-- -----------------------------------------------------------------------------

CREATE TABLE roles (
  id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name        user_role NOT NULL UNIQUE,
  display_name VARCHAR(100) NOT NULL,
  description TEXT,
  permissions JSONB NOT NULL DEFAULT '[]',
  created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  deleted_at  TIMESTAMPTZ
);

CREATE TABLE users (
  id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  email           VARCHAR(255) NOT NULL UNIQUE,
  password_hash   VARCHAR(255) NOT NULL,
  first_name      VARCHAR(100) NOT NULL,
  last_name       VARCHAR(100) NOT NULL,
  phone           VARCHAR(30),
  avatar_url      TEXT,
  role_id         UUID NOT NULL REFERENCES roles(id),
  is_active       BOOLEAN NOT NULL DEFAULT TRUE,
  is_verified     BOOLEAN NOT NULL DEFAULT FALSE,
  mfa_enabled     BOOLEAN NOT NULL DEFAULT FALSE,
  mfa_secret      VARCHAR(255),
  last_login_at   TIMESTAMPTZ,
  locale          VARCHAR(10) DEFAULT 'en',
  created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  deleted_at      TIMESTAMPTZ
);

CREATE INDEX idx_users_email ON users(email) WHERE deleted_at IS NULL;
CREATE INDEX idx_users_role ON users(role_id) WHERE deleted_at IS NULL;

CREATE TABLE refresh_tokens (
  id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id     UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  token_hash  VARCHAR(255) NOT NULL UNIQUE,
  expires_at  TIMESTAMPTZ NOT NULL,
  revoked_at  TIMESTAMPTZ,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  user_agent  TEXT,
  ip_address  INET
);

CREATE INDEX idx_refresh_tokens_user ON refresh_tokens(user_id);
CREATE INDEX idx_refresh_tokens_hash ON refresh_tokens(token_hash);

-- -----------------------------------------------------------------------------
-- ROLE PROFILES
-- -----------------------------------------------------------------------------

CREATE TABLE clients (
  id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id         UUID NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
  address         TEXT,
  city            VARCHAR(100),
  province        VARCHAR(100),
  postal_code     VARCHAR(20),
  date_of_birth   DATE,
  notes           TEXT,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  deleted_at      TIMESTAMPTZ
);

CREATE TABLE lawyers (
  id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id         UUID NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
  bar_number      VARCHAR(50),
  specialization  VARCHAR(255)[],
  bio             TEXT,
  is_available    BOOLEAN NOT NULL DEFAULT TRUE,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  deleted_at      TIMESTAMPTZ
);

CREATE TABLE paralegals (
  id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id         UUID NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
  department      VARCHAR(100),
  supervisor_id   UUID REFERENCES lawyers(id),
  created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  deleted_at      TIMESTAMPTZ
);

-- -----------------------------------------------------------------------------
-- CASES
-- -----------------------------------------------------------------------------

CREATE TABLE case_statuses (
  id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name        VARCHAR(50) NOT NULL UNIQUE,
  display_name VARCHAR(100) NOT NULL,
  color       VARCHAR(20),
  sort_order  INT NOT NULL DEFAULT 0,
  is_terminal BOOLEAN NOT NULL DEFAULT FALSE,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE cases (
  id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  case_number         VARCHAR(30) NOT NULL UNIQUE,
  client_id           UUID NOT NULL REFERENCES clients(id),
  assigned_lawyer_id  UUID REFERENCES lawyers(id),
  assigned_paralegal_id UUID REFERENCES paralegals(id),
  status_id           UUID NOT NULL REFERENCES case_statuses(id),
  category            case_category,
  priority            case_priority NOT NULL DEFAULT 'medium',
  title               VARCHAR(255) NOT NULL,
  description         TEXT,
  intake_summary      TEXT,
  is_actionable       BOOLEAN DEFAULT FALSE,
  formally_proceeded  BOOLEAN NOT NULL DEFAULT FALSE,
  proceeded_at        TIMESTAMPTZ,
  urgency_score       INT DEFAULT 0,
  metadata            JSONB DEFAULT '{}',
  created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  deleted_at          TIMESTAMPTZ
);

CREATE INDEX idx_cases_client ON cases(client_id) WHERE deleted_at IS NULL;
CREATE INDEX idx_cases_lawyer ON cases(assigned_lawyer_id) WHERE deleted_at IS NULL;
CREATE INDEX idx_cases_status ON cases(status_id) WHERE deleted_at IS NULL;
CREATE INDEX idx_cases_category ON cases(category) WHERE deleted_at IS NULL;

CREATE TABLE case_activities (
  id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  case_id     UUID NOT NULL REFERENCES cases(id) ON DELETE CASCADE,
  user_id     UUID REFERENCES users(id),
  action      VARCHAR(100) NOT NULL,
  description TEXT,
  metadata    JSONB DEFAULT '{}',
  created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_case_activities_case ON case_activities(case_id);

-- -----------------------------------------------------------------------------
-- DOCUMENTS
-- -----------------------------------------------------------------------------

CREATE TABLE documents (
  id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  case_id         UUID REFERENCES cases(id),
  uploaded_by     UUID NOT NULL REFERENCES users(id),
  filename        VARCHAR(255) NOT NULL,
  original_name   VARCHAR(255) NOT NULL,
  mime_type       VARCHAR(100) NOT NULL,
  file_size       BIGINT NOT NULL,
  storage_key     TEXT NOT NULL,
  storage_url     TEXT,
  category        VARCHAR(50),
  description     TEXT,
  ocr_text        TEXT,
  ai_summary      TEXT,
  metadata        JSONB DEFAULT '{}',
  is_evidence     BOOLEAN NOT NULL DEFAULT FALSE,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  deleted_at      TIMESTAMPTZ
);

CREATE INDEX idx_documents_case ON documents(case_id) WHERE deleted_at IS NULL;
CREATE INDEX idx_documents_uploader ON documents(uploaded_by) WHERE deleted_at IS NULL;

CREATE TABLE document_embeddings (
  id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  document_id     UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
  chunk_index     INT NOT NULL DEFAULT 0,
  chunk_text      TEXT NOT NULL,
  embedding_id    VARCHAR(255),
  vector_metadata JSONB DEFAULT '{}',
  created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_document_embeddings_doc ON document_embeddings(document_id);

-- -----------------------------------------------------------------------------
-- AI & CHAT
-- -----------------------------------------------------------------------------

CREATE TABLE chats (
  id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  client_id   UUID NOT NULL REFERENCES clients(id),
  case_id     UUID REFERENCES cases(id),
  title       VARCHAR(255),
  is_active   BOOLEAN NOT NULL DEFAULT TRUE,
  metadata    JSONB DEFAULT '{}',
  created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_chats_client ON chats(client_id);

CREATE TABLE chat_messages (
  id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  chat_id     UUID NOT NULL REFERENCES chats(id) ON DELETE CASCADE,
  role        VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
  content     TEXT NOT NULL,
  metadata    JSONB DEFAULT '{}',
  tokens_used INT,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_chat_messages_chat ON chat_messages(chat_id);

CREATE TABLE ai_summaries (
  id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  case_id         UUID REFERENCES cases(id),
  document_id     UUID REFERENCES documents(id),
  summary_type    VARCHAR(50) NOT NULL,
  content         TEXT NOT NULL,
  key_facts       JSONB DEFAULT '[]',
  parties         JSONB DEFAULT '[]',
  evidence_refs   JSONB DEFAULT '[]',
  model_used      VARCHAR(50),
  tokens_used     INT,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_ai_summaries_case ON ai_summaries(case_id);

-- -----------------------------------------------------------------------------
-- TIMELINES & TASKS
-- -----------------------------------------------------------------------------

CREATE TABLE timelines (
  id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  case_id     UUID NOT NULL REFERENCES cases(id) ON DELETE CASCADE,
  event_date  TIMESTAMPTZ NOT NULL,
  title       VARCHAR(255) NOT NULL,
  description TEXT,
  source      VARCHAR(50),
  document_id UUID REFERENCES documents(id),
  metadata    JSONB DEFAULT '{}',
  created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_timelines_case ON timelines(case_id);
CREATE INDEX idx_timelines_date ON timelines(event_date);

CREATE TABLE tasks (
  id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  case_id         UUID NOT NULL REFERENCES cases(id) ON DELETE CASCADE,
  assigned_to     UUID REFERENCES users(id),
  created_by      UUID NOT NULL REFERENCES users(id),
  title           VARCHAR(255) NOT NULL,
  description     TEXT,
  status          task_status NOT NULL DEFAULT 'pending',
  priority        case_priority NOT NULL DEFAULT 'medium',
  due_date        TIMESTAMPTZ,
  completed_at    TIMESTAMPTZ,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  deleted_at      TIMESTAMPTZ
);

CREATE INDEX idx_tasks_case ON tasks(case_id) WHERE deleted_at IS NULL;
CREATE INDEX idx_tasks_assigned ON tasks(assigned_to) WHERE deleted_at IS NULL;

CREATE TABLE comments (
  id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  case_id     UUID NOT NULL REFERENCES cases(id) ON DELETE CASCADE,
  user_id     UUID NOT NULL REFERENCES users(id),
  content     TEXT NOT NULL,
  parent_id   UUID REFERENCES comments(id),
  created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  deleted_at  TIMESTAMPTZ
);

CREATE INDEX idx_comments_case ON comments(case_id) WHERE deleted_at IS NULL;

-- -----------------------------------------------------------------------------
-- NOTIFICATIONS
-- -----------------------------------------------------------------------------

CREATE TABLE notifications (
  id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id     UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  type        notification_type NOT NULL,
  title       VARCHAR(255) NOT NULL,
  body        TEXT,
  data        JSONB DEFAULT '{}',
  is_read     BOOLEAN NOT NULL DEFAULT FALSE,
  read_at     TIMESTAMPTZ,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_notifications_user ON notifications(user_id);
CREATE INDEX idx_notifications_unread ON notifications(user_id, is_read) WHERE is_read = FALSE;

-- -----------------------------------------------------------------------------
-- APPOINTMENTS & PAYMENTS
-- -----------------------------------------------------------------------------

CREATE TABLE appointments (
  id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  case_id     UUID NOT NULL REFERENCES cases(id),
  lawyer_id   UUID REFERENCES lawyers(id),
  client_id   UUID NOT NULL REFERENCES clients(id),
  title       VARCHAR(255) NOT NULL,
  description TEXT,
  scheduled_at TIMESTAMPTZ NOT NULL,
  duration_minutes INT DEFAULT 60,
  location    TEXT,
  is_confirmed BOOLEAN NOT NULL DEFAULT FALSE,
  metadata    JSONB DEFAULT '{}',
  created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  deleted_at  TIMESTAMPTZ
);

CREATE INDEX idx_appointments_case ON appointments(case_id) WHERE deleted_at IS NULL;

CREATE TABLE payments (
  id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  case_id         UUID REFERENCES cases(id),
  client_id       UUID NOT NULL REFERENCES clients(id),
  amount          DECIMAL(12, 2) NOT NULL,
  currency        VARCHAR(3) NOT NULL DEFAULT 'PHP',
  status          payment_status NOT NULL DEFAULT 'pending',
  payment_method  VARCHAR(50),
  reference_number VARCHAR(100) UNIQUE,
  gcash_deeplink  TEXT,
  invoice_number  VARCHAR(50),
  metadata        JSONB DEFAULT '{}',
  paid_at         TIMESTAMPTZ,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_payments_client ON payments(client_id);
CREATE INDEX idx_payments_status ON payments(status);

-- -----------------------------------------------------------------------------
-- AUDIT LOGS
-- -----------------------------------------------------------------------------

CREATE TABLE audit_logs (
  id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id     UUID REFERENCES users(id),
  action      VARCHAR(100) NOT NULL,
  resource    VARCHAR(100),
  resource_id UUID,
  ip_address  INET,
  user_agent  TEXT,
  old_values  JSONB,
  new_values  JSONB,
  metadata    JSONB DEFAULT '{}',
  created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_audit_logs_user ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_action ON audit_logs(action);
CREATE INDEX idx_audit_logs_created ON audit_logs(created_at);

-- -----------------------------------------------------------------------------
-- SEED DATA
-- -----------------------------------------------------------------------------

INSERT INTO roles (name, display_name, description, permissions) VALUES
  ('client', 'Client', 'Law firm client with AI intake access',
   '["chat:read","chat:write","case:read_own","document:upload_own","notification:read"]'),
  ('lawyer', 'Lawyer', 'Licensed attorney with full case management',
   '["case:read","case:write","case:assign","document:read","document:write","ai:use","search:semantic","task:manage"]'),
  ('paralegal', 'Paralegal', 'Legal support staff',
   '["case:read","case:prepare","document:read","document:validate","task:manage","intake:review"]'),
  ('admin', 'Administrator', 'System administrator',
   '["*"]');

INSERT INTO case_statuses (name, display_name, color, sort_order, is_terminal) VALUES
  ('ai_intake', 'AI Intake', '#ec4899', 1, FALSE),
  ('pending_review', 'Pending Review', '#f59e0b', 2, FALSE),
  ('under_review', 'Under Review', '#3b82f6', 3, FALSE),
  ('active', 'Active', '#10b981', 4, FALSE),
  ('on_hold', 'On Hold', '#6b7280', 5, FALSE),
  ('closed', 'Closed', '#374151', 6, TRUE),
  ('declined', 'Declined', '#ef4444', 7, TRUE);

-- Default admin (password: Admin@123456 — change in production)
INSERT INTO users (email, password_hash, first_name, last_name, role_id, is_active, is_verified)
SELECT
  'admin@sansonlaw.ph',
  crypt('Admin@123456', gen_salt('bf', 12)),
  'System',
  'Administrator',
  r.id,
  TRUE,
  TRUE
FROM roles r WHERE r.name = 'admin';
