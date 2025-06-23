FROM ubuntu:22.04

RUN apt-get -qq update && apt-get -qq install -y \
    git \
    python3 python3-pip

# RUN pip install pyTelegramBotAPI
RUN pip install python-telegram-bot
RUN pip install Jinja2 mysql-connector

COPY . /app
COPY ./mydblib /app
COPY ./common /app

CMD ["/usr/bin/python3", "/app/mybot.py"]
