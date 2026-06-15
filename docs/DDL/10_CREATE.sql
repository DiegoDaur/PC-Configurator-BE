-- ============================================================
-- PC Configurator — DDL
-- ============================================================

CREATE TABLE IF NOT EXISTS "user" (
    id       SERIAL PRIMARY KEY,
    username VARCHAR(50)  NOT NULL UNIQUE,
    email    VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role     VARCHAR(10)  NOT NULL DEFAULT 'user'
);

CREATE TABLE IF NOT EXISTS component (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    brand       VARCHAR(50)  NOT NULL,
    category    VARCHAR(20)  NOT NULL,
    price       FLOAT        NOT NULL,
    wattage     INTEGER      NOT NULL DEFAULT 0,
    stock       INTEGER      NOT NULL DEFAULT 0,
    in_stock    BOOLEAN      NOT NULL DEFAULT TRUE,
    image_url   VARCHAR(255),
    description TEXT,
    specs       TEXT
);

CREATE TABLE IF NOT EXISTS compatibility_rule (
    id              SERIAL PRIMARY KEY,
    component_a_id  INTEGER NOT NULL REFERENCES component(id) ON DELETE CASCADE,
    component_b_id  INTEGER NOT NULL REFERENCES component(id) ON DELETE CASCADE,
    is_compatible   BOOLEAN NOT NULL DEFAULT TRUE,
    reason          TEXT,
    CONSTRAINT no_self_rule CHECK (component_a_id <> component_b_id)
);

CREATE TABLE IF NOT EXISTS build (
    id         SERIAL PRIMARY KEY,
    user_id    INTEGER      NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
    name       VARCHAR(100) NOT NULL,
    notes      TEXT,
    created_at TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS build_component (
    id           SERIAL PRIMARY KEY,
    build_id     INTEGER NOT NULL REFERENCES build(id) ON DELETE CASCADE,
    component_id INTEGER NOT NULL REFERENCES component(id) ON DELETE RESTRICT
);
