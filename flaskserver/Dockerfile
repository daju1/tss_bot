FROM ubuntu:22.04

RUN apt-get -qq update && apt-get -qq install -y \
    git \
    python3 python3-pip

# flask
# RUN pip install -r requirements.txt

#FROM python:3.12

RUN apt-get update
RUN apt-get -y install net-tools iproute2 iputils-ping

#WORKDIR /app
COPY requirements.txt .

#RUN pip install -r requirements.txt
#RUN pip install pandas flask-WTF
RUN pip install flask flask-login flask-WTF flask-httpauth passlib
RUN pip install Jinja2 mysql-connector

COPY . /app
COPY ./mydblib /app/
COPY ./common /app

CMD ["/app/start_flask.sh"]
