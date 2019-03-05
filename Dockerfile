FROM node:8.15.0-alpine

MAINTAINER Dhaval Metrani <dhavalmetrani@gmail.com>

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
RUN adduser -h /healthbot -s /bin/bash -S healthbot
USER  healthbot
WORKDIR /healthbot

COPY ./requirements.txt /healthbot/requirements.txt
RUN pip install -r requirements.txt --user

# Install hubot
RUN yo hubot --owner="Dhaval Metrani <dhavalmetrani@gmail.com>" --name="healthbot" \
  --description="Healthbot for health related autmoations." --defaults \
   && npm install hubot-slack --save

COPY ./bash /healthbot/bash
COPY ./src /healthbot/src
COPY ./external-scripts.json /healthbot/
COPY ./scripts/healthbot.coffee /healthbot/scripts/

# And go
CMD ["/bin/sh", "-c", "bin/hubot --adapter slack"]
