#!/bin/sh

echo "Apagando dispositivos..."
sqlite3 ysto.db "delete from Devices"
