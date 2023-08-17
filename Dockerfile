FROM 818476207984.dkr.ecr.us-west-2.amazonaws.com/advancedthreatanalytics/python-slim:latest
MAINTAINER infrastructure@advancedthreatanalytics.com

COPY reports /opt/app/reports/
COPY setup.py tox.ini /opt/app/

RUN pip install tox

WORKDIR /opt/app