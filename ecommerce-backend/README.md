# alx-project-nexus / ecommerce-backend

Lean, production-ready Django eCommerce backend.

Quickstart:
1. Copy `.env.example` to `.env` and edit DB/SECRET settings.
2. `docker-compose up --build`
3. API: http://localhost:8000/api/
4. Swagger: http://localhost:8000/swagger/
5. GraphQL: http://localhost:8000/graphql/

Run tests:
- Locally (inside container): `docker-compose exec web python manage.py test`
