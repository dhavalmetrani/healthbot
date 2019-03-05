CONATINER_NAME=healthbot
CONTAINER_VERSION=latest

help:            ## Show this help.
	@grep -h "##" $(MAKEFILE_LIST) | grep -v grep | sed -e 's/\\$$//' | sed -e 's/##//'

build:           ## Build the docker container.
	docker build -t $(CONATINER_NAME) .

run:             ## Run the docker container.
	$(MAKE) build
	@docker run --env HUBOT_SLACK_TOKEN=${HEALTHBOT_SLACK_TOKEN} $(CONATINER_NAME):$(CONTAINER_VERSION)

ps:              ## Check the running containers.
	docker ps
