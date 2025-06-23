#!/bin/sh
#

cp -fr ./mydblib/ ./flaskserver/
cp -fr ./common/ ./flaskserver/
cp -fr ./mydblib/ ./python-telegram-bot/
cp -fr ./common/ ./python-telegram-bot/

docker compose build

rm -r ./flaskserver/mydblib/
rm -r ./flaskserver/common/
rm -r ./python-telegram-bot/mydblib/
rm -r ./python-telegram-bot/common/
