REQ-PAY-1: Repeated requests with the same idempotency key must create at most one durable payment operation and return the same operation ID.
Payments.rows represents the durable ledger in this minimal fixture. Use python3 -m unittest -v.
