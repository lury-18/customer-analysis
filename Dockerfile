# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /front-end

COPY requirements.txt requirements.txt
COPY dashboard-delivery.py dashboard-delivery.py
COPY dashboard-reco.py dashboard-reco.py
RUN pip3 install -r requirements.txt


ENTRYPOINT ["python"]