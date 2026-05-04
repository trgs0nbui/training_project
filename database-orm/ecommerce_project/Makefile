.PHONY: help build up down logs migrate shell createsuperuser clean ps exec

help:
	@echo "=== Django + Docker Makefile Commands ==="
	@echo ""
	@echo "Docker Commands:"
	@echo "  make build          - Build Docker images"
	@echo "  make up             - Start services (daemonized)"
	@echo "  make down           - Stop services"
	@echo "  make ps             - Show running services"
	@echo "  make logs           - Show all logs (follow mode)"
	@echo "  make logs-web       - Show Django logs"
	@echo "  make logs-db        - Show PostgreSQL logs"
	@echo "  make logs-nginx     - Show Nginx logs"
	@echo "  make clean          - Remove containers and volumes"
	@echo ""
	@echo "Django Commands:"
	@echo "  make migrate        - Run database migrations"
	@echo "  make makemigrations - Create new migrations"
	@echo "  make shell          - Django shell"
	@echo "  make createsuperuser - Create admin user"
	@echo "  make collectstatic  - Collect static files"
	@echo ""
	@echo "Database Commands:"
	@echo "  make db-shell       - PostgreSQL shell"
	@echo "  make db-backup      - Backup database"
	@echo "  make db-reset       - Reset database (DELETE DATA!)"
	@echo ""
	@echo "Development:"
	@echo "  make requirements   - Update requirements.txt"
	@echo "  make test           - Run tests"
	@echo "  make lint           - Run linters"
	@echo ""

# Docker
build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose stop

ps:
	docker-compose ps

logs:
	docker-compose logs -f

logs-web:
	docker-compose logs -f web

logs-db:
	docker-compose logs -f db

logs-nginx:
	docker-compose logs -f nginx

clean:
	docker-compose down
	docker volume prune -f

# Django Management
migrate:
	docker-compose exec web python manage.py migrate

makemigrations:
	docker-compose exec web python manage.py makemigrations

shell:
	docker-compose exec web python manage.py shell

createsuperuser:
	docker-compose exec web python manage.py createsuperuser

collectstatic:
	docker-compose exec web python manage.py collectstatic --noinput

check:
	docker-compose exec web python manage.py check

# Database
db-shell:
	docker-compose exec db psql -U $$(grep POSTGRES_USER .env | cut -d '=' -f2) -d $$(grep POSTGRES_DB .env | cut -d '=' -f2)

db-backup:
	docker-compose exec db pg_dump -U $$(grep POSTGRES_USER .env | cut -d '=' -f2) $$(grep POSTGRES_DB .env | cut -d '=' -f2) > backup_$$(date +%Y%m%d_%H%M%S).sql

db-reset:
	@echo "⚠️  WARNING: This will DELETE all data!"
	@echo "Press Ctrl+C to cancel, or wait 5 seconds..."
	@sleep 5
	docker-compose down -v
	docker-compose up -d
	docker-compose exec web python manage.py migrate
	@echo "Database reset complete!"

# Development
requirements:
	docker-compose exec web pip freeze > requirements.txt

test:
	docker-compose exec web python manage.py test

lint:
	docker-compose exec web python -m flake8 .
	docker-compose exec web python -m black --check .

format:
	docker-compose exec web python -m black .

# Utilities
health:
	@echo "Checking health..."
	@curl -s http://localhost:8000/health | python -m json.tool || echo "Service not responding"

restart:
	docker-compose restart

exec:
	docker-compose exec web bash

install-packages:
	docker-compose exec web pip install -r requirements.txt

# Setup
setup: build up migrate createsuperuser
	@echo "✓ Setup complete!"
	@echo "Login at: http://localhost/admin"

# Development setup
dev-setup: up migrate
	@echo "✓ Development setup complete!"
	@echo "Start developing at: http://localhost:8000"

.DEFAULT_GOAL := help
