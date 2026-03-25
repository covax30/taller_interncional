# Desarrollo
dev-up:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml --env-file .env.dev up

dev-up-build:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml --env-file .env.dev up --build

dev-down:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml down

dev-exec:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml exec web $(cmd)

superuser:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml exec web python manage.py createsuperuser

migrate:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml exec web python manage.py migrate

# Producción
prod-up:
	docker compose -f docker-compose.yml -f docker-compose.prod.yml --env-file .env.prod up -d

prod-down:
	docker compose -f docker-compose.yml -f docker-compose.prod.yml down