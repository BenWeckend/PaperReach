DOCS_PATH=$(shell pwd)/docs/build
IMAGE_NAME=sphinx-docs

.PHONY: html build run

html: build run

build:
	docker build -t $(IMAGE_NAME) .


run:
	docker run --rm -v $(DOCS_PATH):/app/docs/build $(IMAGE_NAME)
