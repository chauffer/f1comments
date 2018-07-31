FROM python:3.7-alpine3.7

WORKDIR /app

COPY ./requirements.txt /app
RUN apk --no-cache --virtual=.build-deps add build-base musl-dev &&\
    SANIC_NO_UVLOOP=true pip install -r requirements.txt &&\
    apk --purge del .build-deps

COPY . /app

RUN pip install -e .

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
CMD ["f1comments"]
LABEL name=f1comments version=dev \
      maintainer="Simone Esposito <chaufnet@gmail.com>"
