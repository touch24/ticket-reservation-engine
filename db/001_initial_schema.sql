BEGIN;

CREATE TYPE reservation_status AS ENUM(
    'PENDING', 
    'CONFIRMED', 
    'EXPIRED', 
    'CANCELLED'
);

CREATE TYPE payment_status AS ENUM(
    'PROCESSING', 
    'SUCCEEDED', 
    'FAILED', 
    'REFUNDED'
);



CREATE TABLE users (
    "id" BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    "public_id" UUID DEFAULT gen_random_uuid() NOT NULL UNIQUE,
    "email" VARCHAR(255) NOT NULL UNIQUE,
    "full_name" VARCHAR(100) NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE ticket_types (
    "id" BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    "public_id" UUID DEFAULT gen_random_uuid() NOT NULL UNIQUE,
    "name" VARCHAR(100) NOT NULL,
    "total_capacity" INT NOT NULL CHECK (total_capacity > 0),
    "price_in_cents" INT NOT NULL CHECK (price_in_cents >= 0),
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE reservations (
    "id" BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    "public_id" UUID DEFAULT gen_random_uuid() NOT NULL UNIQUE,
    "user_id" BIGINT NOT NULL,
    "ticket_type_id" BIGINT NOT NULL,
    "status" reservation_status NOT NULL DEFAULT 'PENDING',
    "expires_at" TIMESTAMPTZ NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_reservations_user_id
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_reservations_ticket_type_id
        FOREIGN KEY (ticket_type_id)
        REFERENCES ticket_types (id)
        ON DELETE RESTRICT
);

CREATE TABLE payments(
    "id" BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    "public_id" UUID DEFAULT gen_random_uuid() NOT NULL UNIQUE,
    "reservation_id" BIGINT NOT NULL,
    "idempotency_key" VARCHAR(255) NOT NULL UNIQUE,
    "amount_in_cents" INT NOT NULL CHECK (amount_in_cents >= 0),
    "status" payment_status DEFAULT 'PROCESSING' NOT NULL,
    "created_at" TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,

    CONSTRAINT fk_payments_reservation_id
        FOREIGN KEY ("reservation_id")
        REFERENCES reservations(id)
        ON DELETE RESTRICT
);

CREATE TABLE tickets(
    "id" BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    "public_id" UUID DEFAULT gen_random_uuid() NOT NULL UNIQUE,
    "reservation_id" BIGINT NOT NULL,
    "user_id" BIGINT NOT NULL,
    "ticket_type_id" BIGINT NOT NULL,
    "ticket_code" VARCHAR(64) NOT NULL UNIQUE,
    "issued_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_tickets_user_id
        FOREIGN KEY ("user_id")
        REFERENCES "users"("id")
        ON DELETE RESTRICT,

    CONSTRAINT fk_tickets_reservation_id
        FOREIGN KEY ("reservation_id")
        REFERENCES "reservations"("id")
        ON DELETE RESTRICT,

    CONSTRAINT fk_tickets_ticket_type_id
        FOREIGN KEY ("ticket_type_id")
        REFERENCES "ticket_types" ("id")
        ON DELETE RESTRICT
);

COMMIT;