APP_DIR := /code
APP_NAME := web
SETTINGS_PATH := banc.settings


test-dev:
	pytest --ds=$(SETTINGS_PATH)

run-dev:
	python3 manage.py runserver

test-prod: build
	sudo docker-compose run --rm -- $(APP_NAME) pytest --ds=$(SETTINGS_PATH)

run-prod:
	sudo docker-compose up -d --build

build:
	sudo docker-compose build

