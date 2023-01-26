FROM python:3.11.1-slim as build

RUN apt-get update && apt-get install --yes --no-install-recommends make

# NOTE(krishan711): libmagc required specifically for pablo
RUN apt-get update \
    && apt-get install -y --no-install-recommends libmagic-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY makefile $WORKDIR

# Install requirements
COPY requirements-dev.txt $WORKDIR
COPY requirements.txt $WORKDIR
RUN make install

COPY . $WORKDIR

EXPOSE 5000
CMD ["make", "start-prod"]
