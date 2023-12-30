#!/bin/bash

VARIABLE=$1
# Получаем полный путь до директории, где находится этот скрипт
SCRIPT_DIR=$(dirname $(readlink -f "$0"))

# Создаем systemd service файл
cat <<EOF > /etc/systemd/system/marzban-$VARIABLE.service
[Unit]
Description=Marzban $VARIABLE
After=multi-user.target

[Service]
Type=simple
Restart=always
ExecStart=/usr/bin/python3 $SCRIPT_DIR/$VARIABLE.py

[Install]
WantedBy=multi-user.target
EOF

# Перезагрузка systemd, включение и запуск сервиса
systemctl daemon-reload
systemctl enable marzban-$VARIABLE.service
systemctl start marzban-$VARIABLE.service
systemctl status marzban-$VARIABLE.service
