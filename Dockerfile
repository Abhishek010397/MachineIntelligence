FROM alpine:latest

ARG VERSION=0.0.0

ENV PYTHONBUFFERED=1

RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python

RUN apk add make && apk add tree

RUN python3 -m ensurepip && pip3 install --no-cache --upgrade pip setuptools

RUN pip install sphinx-rtd-theme && pip install Sphinx 

RUN mkdir docs && cd docs && sphinx-quickstart -q --ext-autodoc -p MODBUS -a i4sens.com && cd ..

RUN rm -f docs/conf.py && rm -f docs/index.rst && ls docs/

COPY documentation/* docs/
COPY  sample/* docs/  

RUN cd docs && make html && cd _build/html && pip install awscli

RUN cd docs/_build/html && aws --version

RUN cd docs/_build/html && aws s3 sync . s3://sphinx-pydocs/Modbus/v$VERSION/



