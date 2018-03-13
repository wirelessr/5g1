PROJECT_NAME=5g1

GIT_BRANCH=$(shell echo `git rev-parse --abbrev-ref HEAD`)
GIT_COMMIT=$(shell git rev-parse --short HEAD)
DOCKER_IMAGE_VERSION=$(GIT_BRANCH)-$(GIT_COMMIT)
DOCKER_IMAGE_NAME=$(PROJECT_NAME):$(DOCKER_IMAGE_VERSION)

HOST_PORT=80
CONTAINER_PORT=80

CURRENT_DIR=$(shell pwd)
MOUNT_LOCAL_DIR=$(CURRENT_DIR)/app
CONTAINER_WORK_DIR=/app

install-requirements:
	pip3 install -r requirements.txt

run:
	python3 5g1/main.py

docker_build:
	docker build -t $(DOCKER_IMAGE_NAME) .
	docker tag $(DOCKER_IMAGE_NAME) $(PROJECT_NAME):latest

docker_run:
	docker run -it -p $(HOST_PORT):$(CONTAINER_PORT) $(DOCKER_IMAGE_NAME) /bin/bash

docker_runserver:
	docker run -it -p $(HOST_PORT):$(CONTAINER_PORT) $(DOCKER_IMAGE_NAME)

docker_runserver_mount_local:
	docker run -it -p $(HOST_PORT):$(CONTAINER_PORT) -v $(MOUNT_LOCAL_DIR):$(CONTAINER_WORK_DIR) $(DOCKER_IMAGE_NAME)
