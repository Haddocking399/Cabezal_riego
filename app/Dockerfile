# syntax=docker/dockerfile:1.4

FROM --platform=$BUILDPLATFORM python:3.10-slim AS builder
EXPOSE 8000
WORKDIR /app 
COPY requirements.txt /app
COPY docker-entrypoint.sh /app
RUN apt-get update
RUN apt-get install -y gcc
RUN apt-get install -y default-libmysqlclient-dev
ENV PYTHONBUFFERED 1
RUN pip install -r requirements.txt --no-cache-dir
COPY . /app 
CMD /app/docker-entrypoint.sh

FROM builder as dev-envs
RUN <<EOF
apk update
apk add git
EOF

RUN <<EOF
addgroup -S docker
adduser -S --shell /bin/bash --ingroup docker vscode
EOF
# install Docker tools (cli, buildx, compose)
COPY --from=gloursdocker/docker / /