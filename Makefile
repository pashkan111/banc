APP_DIR := /code
APP_NAME := web
SETTINGS_PATH := banc.settings


.PHONY: test
test:
	sudo docker-compose run --rm -- $(APP_NAME) pytest --ds=$(SETTINGS_PATH)

.PHONY: run
run:
	sudo docker-compose up --force-recreate --build $(APP_NAME)

.PHONY: build
build:
	sudo docker-compose build
