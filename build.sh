#!/bin/sh
#

cp -fr ./mydblib/ ./flaskserver/
cp -fr ./static/ ./flaskserver/
cp -fr ./mydblib/ ./python-telegram-bot/
cp -fr ./static/ ./python-telegram-bot/

docker compose build

rm -r ./flaskserver/mydblib/
rm -r ./flaskserver/static/
rm -r ./python-telegram-bot/mydblib/
rm -r ./python-telegram-bot/static/
