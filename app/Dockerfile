FROM debian:stretch

WORKDIR /app

VOLUME [ "/app" ]

RUN apt-get update
RUN apt-get -yq install \
    locales \
    ca-certificates \
    curl \
    build-essential \
    \
    python3 \
    python3-cffi \
    cython3 \
    python3-pip \
    python3-wheel \
    python3-setuptools \
    python3-dev \
    python3-requests \
    python3-psycopg2

RUN apt-get -yq install osm2pgrouting postgresql-client

RUN pip3 install Django djangorestframework django-cors-headers gunicorn

CMD ["./run_prod.sh"]
