FROM alpine:latest

RUN apk update && apk upgrade && apk add sudo

ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools

RUN apk --no-cache add curl && apk add curl-doc

RUN curl "https://s3.amazonaws.com/aws-cli/awscli-bundle.zip" -o "awscli-bundle.zip"

RUN unzip -o awscli-bundle.zip 

RUN sudo ./awscli-bundle/install -i /usr/local/aws -b /usr/local/bin/aws

RUN aws --version
