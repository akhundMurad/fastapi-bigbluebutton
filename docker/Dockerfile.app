FROM python:3.9-alpine

WORKDIR /app/

COPY ../requirements.txt /src/requirements.txt

COPY .. .

RUN apk add gcc g++ libffi-dev

RUN python -m pip --no-cache-dir install --upgrade pip
RUN pip install -r requirements.txt