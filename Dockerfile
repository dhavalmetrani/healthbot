FROM node:8.15.0-alpine

MAINTAINER Dhaval Metrani <dhavalmetrani@gmail.com>
ARG SERVICE_USER=healthbot

# Install pre-requisites.
RUN apk update \
  && apk add build-base libffi-dev openssl-dev \
  && apk add python3 python3-dev \
  && ln -s /usr/bin/python3 /usr/bin/python \
  && apk add curl \
  && curl -sS https://bootstrap.pypa.io/get-pip.py | python3 \
  && apk --purge -v del py-pip \
  && rm -rf /var/cache/apk/* \
  && npm install -g hubot coffeescript yo generator-hubot

# Create healthbot user
RUN adduser -h /${SERVICE_USER} -s /bin/bash -S ${SERVICE_USER}
USER  ${SERVICE_USER}
WORKDIR /${SERVICE_USER}

COPY ./requirements.txt /${SERVICE_USER}/requirements.txt
RUN pip install -r requirements.txt --user

# Install hubot
RUN yo hubot --owner="Dhaval Metrani <dhavalmetrani@gmail.com>" --name="${SERVICE_USER}" \
  --description="Healthbot for health related autmoations." --defaults \
   && npm install hubot-slack --save

COPY ./bash /${SERVICE_USER}/bash
COPY ./src /${SERVICE_USER}/src
COPY ./external-scripts.json /${SERVICE_USER}/
COPY ./scripts/${SERVICE_USER}.coffee /${SERVICE_USER}/scripts/

# And go
CMD ["/bin/sh", "-c", "bin/hubot --adapter slack"]
