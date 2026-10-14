BEGIN;

ALTER TABLE tickets 
    ADD CONSTRAINT uq_tickets_reservation_id UNIQUE (reservation_id);

CREATE INDEX IF NOT EXISTS idx_reservations_user_id ON reservations (user_id);
CREATE INDEX IF NOT EXISTS idx_reservations_ticket_type_id ON reservations (ticket_type_id);
CREATE INDEX IF NOT EXISTS idx_payments_reservation_id ON payments (reservation_id);
CREATE INDEX IF NOT EXISTS idx_tickets_user_id ON tickets (user_id);

CREATE INDEX IF NOT EXISTS idx_reservations_status_expires_at ON reservations (status, expires_at);

COMMIT;