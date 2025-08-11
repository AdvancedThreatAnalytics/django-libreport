FROM 818476207984.dkr.ecr.us-west-2.amazonaws.com/advancedthreatanalytics/python-slim:3.13-build
LABEL maintainer="Critical Start <infrastructure@advancedthreatanalytics.com>"

ARG PIP_INDEX_URL

RUN pip install tox

COPY reports /opt/app/reports/
COPY setup.py tox.ini /opt/app/

WORKDIR /opt/app
