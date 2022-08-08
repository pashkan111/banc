APP_DIR := /code
APP_NAME := web
SETTINGS_PATH_PROD := banc.settings_prod
SETTINGS_PATH_DEV := banc.settings_dev


.PHONY: run
run-dev:
	python3 manage.py runserver

.PHONY: test
test-prod:
	sudo docker-compose run --rm -- $(APP_NAME) pytest --ds=$(SETTINGS_PATH)

.PHONY: run
run-prod:
	sudo docker-compose up --force-recreate --build $(APP_NAME)

.PHONY: build
build-prod:
	sudo docker-compose build
