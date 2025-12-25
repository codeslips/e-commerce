.PHONY: up dev stop db-init db-migrate clean logs

# Docker compose command (use 'docker compose' for newer Docker versions)
DOCKER_COMPOSE := docker compose

# Default target
all: up

# Start all services in production mode
up:
	$(DOCKER_COMPOSE) up --build -d

# Start development mode with hot reload
dev:
	$(DOCKER_COMPOSE) up --build

# Stop all services
stop:
	$(DOCKER_COMPOSE) down

# Initialize database (create tables)
db-init:
	$(DOCKER_COMPOSE) exec backend python -m scripts.init_db

# Run database migrations
db-migrate:
	$(DOCKER_COMPOSE) exec backend alembic upgrade head

# View logs
logs:
	$(DOCKER_COMPOSE) logs -f

# Clean up everything (including volumes)
clean:
	$(DOCKER_COMPOSE) down -v
	docker system prune -f

# Rebuild without cache
rebuild:
	$(DOCKER_COMPOSE) build --no-cache
	$(DOCKER_COMPOSE) up -d

# Show status
status:
	$(DOCKER_COMPOSE) ps

# Backend shell
shell:
	$(DOCKER_COMPOSE) exec backend /bin/sh

# Frontend shell
shell-frontend:
	$(DOCKER_COMPOSE) exec frontend /bin/sh

# Database shell
shell-db:
	$(DOCKER_COMPOSE) exec db psql -U xinyutian -d xinyutian

# Seed database with demo data
seed:
	$(DOCKER_COMPOSE) exec backend python -m scripts.seed_data
