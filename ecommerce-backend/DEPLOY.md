# Deploy & Demo

## Local (Docker Compose)
1. Copy `.env.example` to `.env` and adjust.
2. `docker-compose up --build`
3. API: http://localhost:8000/api/
4. Swagger: http://localhost:8000/swagger/
6. Start Celery worker and beat (if not already):
	- `docker-compose up -d celery celery-beat`
7. To run the seed data:
	- `docker-compose exec web python manage.py seed`
5. Seed demo: `docker-compose exec web python manage.py seed`

## Render (example)
- Create a service, set build to use `ecommerce-backend/Dockerfile`
- Provide environment variables
- Use worker for celery commands
 - Jenkins: add credentials `DB_NAME`, `DB_USER`, `DB_PASS`, `SECRET_KEY` (type: Secret text)
	 The provided `Jenkinsfile` will write a runtime `ecommerce-backend/.env` and run `docker-compose up --build -d`.

## Verification
- Register or create user in admin
- Obtain JWT token: POST /api/auth/token/ with email/password
- Use token to create protected resources
