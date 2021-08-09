FROM 2307297/pymodbus:latest

ARG VERSION=0.0.0

ENV PYTHONBUFFERED=1

RUN mkdir sphinx-docs && cd sphinx-docs && sphinx-quickstart -q --ext-autodoc -p MODBUS -a i4sens.com 

RUN rm -f conf.py && rm -f index.rst 

RUN rm -rf source && mkdir sphinx-docs/source 

COPY documentation/* sphinx-docs/    

COPY Modbus/* sphinx-docs/source/

COPY modbus_config.json sphinx-docs/source/modbus_config.json

COPY Simulation/* sphinx-docs/source/

RUN cd sphinx-docs && sphinx-apidoc -o rst source && make clean && make html  

RUN cd sphinx-docs/_build/html  && aws s3 sync . s3://sphinx-pydocs/Modbus/$VERSION




