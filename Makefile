PROJECT_NAME=5g1

GIT_BRANCH=$(shell echo `git rev-parse --abbrev-ref HEAD`)
GIT_COMMIT=$(shell git rev-parse --short HEAD)
DOCKER_IMAGE_VERSION=$(GIT_BRANCH)-$(GIT_COMMIT)
DOCKER_IMAGE_NAME=$(PROJECT_NAME):$(DOCKER_IMAGE_VERSION)


install-requirements:
	pip3 install -r requirements.txt

run:
	python3 5g1/main.py

docker_build:
	docker build -t $(DOCKER_IMAGE_NAME) .
	docker tag $(DOCKER_IMAGE_NAME) $(PROJECT_NAME):latest
