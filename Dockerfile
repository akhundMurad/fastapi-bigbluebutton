FROM python:3.9-alpine

WORKDIR /app/

COPY requirements.txt /src/requirements.txt

COPY . .

RUN pip install -r requirements.txt