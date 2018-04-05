FROM debian:stretch

WORKDIR /app

VOLUME [ "/app" ]

# sudo apt-get install build-essential python3-dev python3-pip python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info
# Mapnik > Weasyprint > mapnik > weasyprint > mapnik
RUN apt-get update && \
apt-get -yq install \
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
    python3-psycopg2 \
    libprotobuf-dev \
    libleveldb-dev \
    libgeos-dev \
    postgresql-client-9.6

RUN apt-get -yq install osm2pgrouting

RUN apt-get -yq install gdal-bin

RUN pip3 install Django djangorestframework django-cors-headers gunicorn polyline

CMD ["./run_prod.sh"]
