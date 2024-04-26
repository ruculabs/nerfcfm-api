# Define variables
DOCKER_COMPOSE_FILE = docker-compose.yml

.PHONY: up
up: ## Start the Docker containers
	docker-compose -f $(DOCKER_COMPOSE_FILE) up --build

.PHONY: down
down: ## Stop and remove the Docker containers
	docker-compose -f $(DOCKER_COMPOSE_FILE) down

.PHONY: test
test: ## Run tests
	docker-compose -f $(DOCKER_COMPOSE_FILE) exec web python manage.py test

.PHONY: clean
clean: ## Remove Docker images and clean up
	docker-compose -f $(DOCKER_COMPOSE_FILE) down --rmi all

