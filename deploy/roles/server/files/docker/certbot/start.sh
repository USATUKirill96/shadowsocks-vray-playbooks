#!/bin/sh

echo "Генерация сертификата"
/usr/bin/cron-task.sh

echo "Запуск генерации по таймеру"
exec crond -f