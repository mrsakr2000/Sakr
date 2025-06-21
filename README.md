# VPS Reseller Platform Backend

This project provides a simple Flask-based backend to provision VPS servers via the Contabo API after PayPal payment. A basic user authentication flow, PayPal IPN endpoint, and email notifications are included.

## Setup

1. Create a virtual environment and install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Copy `.env.example` to `.env` and fill in the credentials.

3. Run the application:

```bash
python run.py
```

## Endpoints

- `POST /auth/register` – Register a new user with JSON `{"email": "...", "password": "..."}`
- `POST /auth/login` – Log in a user
- `GET /vps/plans` – List available VPS plans (requires login)
- `POST /vps/create` – Provision a VPS after payment (requires login)
- `GET /vps/` – List current user's VPS
- `GET /vps/<id>` – Get details for a specific VPS
- `POST /payments/ipn` – PayPal IPN endpoint
- `GET /payments/invoices` – List user's invoices

A Postman collection is provided in `postman_collection.json`.
