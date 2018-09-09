FROM resin/raspberry-pi-alpine-python:3.6
MAINTAINER Jose Ortiz "jlortiz@uc.cl"
COPY . /usr/src/app
WORKDIR /usr/src/app
RUN make venv
ENTRYPOINT ["make", "run"]