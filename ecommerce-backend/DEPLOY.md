# Deploy & Demo

## Local (Docker Compose)
1. Copy `.env.example` to `.env` and adjust.
2. `docker-compose up --build`
3. API: http://localhost:8000/api/
4. Swagger: http://localhost:8000/swagger/
5. Seed demo: `docker-compose exec web python manage.py seed`

## Render (example)
- Create a service, set build to use `ecommerce-backend/Dockerfile`
- Provide environment variables
- Use worker for celery commands

## Verification
- Register or create user in admin
- Obtain JWT token: POST /api/auth/token/ with email/password
- Use token to create protected resources
