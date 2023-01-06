.DEFAULT_GOAL := help
help:
	@perl -nle'print $& if m{^[a-zA-Z_-]+:.*?## .*$$}' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-25s\033[0m %s\n", $$1, $$2}'

django: ## runs the django container
	docker-compose -f local.yml up --detach --build --remove-orphans django

postgres: ## runs the postgres container
	docker-compose -f local.yml up --detach postgres

build: ## builds the platform locally
	docker-compose -f local.yml build

up: ## runs all docker containers
	docker-compose -f local.yml up --build -d

stop: ## stops all docker containers
	docker-compose -f local.yml stop

django-logs: ## attach to logs
	docker-compose -f local.yml logs -f django

logs: ## attach to logs
	docker-compose -f local.yml logs -f

migrations: ## make migration files
	docker-compose -f local.yml run django python manage.py makemigrations
	find . -print | grep -i "./aquaticode/.*/migrations/" | xargs -d '\n' sudo chown eracle:eracle

migrate: ## migrate db
	docker-compose -f local.yml run django python manage.py migrate

bash-django: ## launches a console on the django instance
	docker-compose -f local.yml run django bash

test: ## runs tests
	docker-compose -f local.yml run django py.test --cache-clear
