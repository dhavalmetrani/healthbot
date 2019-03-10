CONATINER_NAME=healthbot
CONTAINER_VERSION=`cat VERSION`
DOCKER_REGISTRY_URL=docker.io

help:                      ## Show this help.
	@grep -h "##" $(MAKEFILE_LIST) | grep -v grep | tr -d '##' | tr -d '$$'

release-patch:             ## Tag the release as a patch release and push tag to git.
	./sem_ver.sh VERSION release-patch

release-minor:             ## Tag the release as a minor  releaseand push tag to git.
	./sem_ver.sh VERSION release-minor

release-major:             ## Tag the release as a major release and push tag to git.
	./sem_ver.sh VERSION release-major

docker-build:              ## Build the docker container.
	docker build -t $(CONATINER_NAME) .

docker-login:              ## Login to docker public registry.
	@docker login -u ${DOCKER_USER} -p ${DOCKER_PASSWORD} $(DOCKER_REGISTRY_URL)

docker-run:                ## Run the docker container.
	$(MAKE) build
	@docker run --env HUBOT_SLACK_TOKEN=${HEALTHBOT_SLACK_TOKEN} $(CONATINER_NAME):$(CONTAINER_VERSION)

docker-ps:                 ## Check the running containers.
	docker ps

docker-publish:            ## Publish the docker image to registry using existing version.
	docker tag $(CONATINER_NAME) ${DOCKER_USER}/$(CONATINER_NAME):$(CONTAINER_VERSION)
	docker push $(DOCKER_REGISTRY_URL)/${DOCKER_USER}/$(CONATINER_NAME):$(CONTAINER_VERSION)

docker-publish-patch:      ## Publish the docker image to registry by tagging as a patch release to git.
	$(MAKE) release-patch
	docker tag $(CONATINER_NAME) ${DOCKER_USER}/$(CONATINER_NAME):$(CONTAINER_VERSION)
	docker push $(DOCKER_REGISTRY_URL)/${DOCKER_USER}/$(CONATINER_NAME):$(CONTAINER_VERSION)

docker-publish-minor:      ## Publish the docker image to registry by tagging as a minor release to git.
	$(MAKE) release-minor
	docker tag $(CONATINER_NAME) ${DOCKER_USER}/$(CONATINER_NAME):$(CONTAINER_VERSION)
	docker push $(DOCKER_REGISTRY_URL)/${DOCKER_USER}/$(CONATINER_NAME):$(CONTAINER_VERSION)

docker-publish-major:      ## Publish the docker image to registry by tagging as a major release to git.
	$(MAKE) release-major
	docker tag $(CONATINER_NAME) ${DOCKER_USER}/$(CONATINER_NAME):$(CONTAINER_VERSION)
	docker push $(DOCKER_REGISTRY_URL)/${DOCKER_USER}/$(CONATINER_NAME):$(CONTAINER_VERSION)
