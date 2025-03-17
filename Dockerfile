FROM python:3.12

WORKDIR /app

COPY requirements-dev.txt requirements-dev.txt

RUN pip install -r requirements-dev.txt

COPY . .
