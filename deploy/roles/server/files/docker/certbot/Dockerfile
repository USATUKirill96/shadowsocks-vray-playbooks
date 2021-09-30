FROM alpine:3.14

RUN apk --no-cache update && \
    apk --no-cache upgrade && \
    apk --no-cache add \
      certbot 

# Копируем скрипт с запуском генерации сертификата
COPY ./certbot/cron-task.sh /usr/bin/cron-task.sh
COPY ./certbot/start.sh /start.sh

# Права на запуск
RUN chmod +x /usr/bin/cron-task.sh
RUN chmod +x /start.sh

# Добавляем запуск скрипта раз в месяц в конфиг крона
RUN echo "0 0 1 * * /usr/bin/cron-task.sh" > /etc/crontabs/root

ENTRYPOINT ["/start.sh"]