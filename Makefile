DOCKER_IMAGE_NAME = nerfcfm-api

.PHONY: build
build: ## Build the Docker image
	docker build -t $(DOCKER_IMAGE_NAME) .

.PHONY: run
run: ## Run the Docker container
	docker run --rm -it -p 8000:8000 $(DOCKER_IMAGE_NAME)

.PHONY: test
test: ## Run tests
	python manage.py test

.PHONY: clean
clean: ## Remove Docker image and clean up
	docker image rm $(DOCKER_IMAGE_NAME)

