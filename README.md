# healthbot
Healthbot helps you with health related things.

## More on slackbot
- Refer Dockerfile

## Prerequisites
- Python 3.7 (I prefer virtualenv)
- Docker

## Setup
Set the following environment variables:
```
HEALTHBOT_SLACK_TOKEN="xoxb-xxxx"
```

## Run locally
Run the following make command:
```
make run
```

## Stop the container
Run the following command. It will stop all containers running locally.
```
docker stop `docker container ls -q`
```
