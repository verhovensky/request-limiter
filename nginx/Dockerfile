FROM nginx:alpine
RUN apk add --no-cache esh openssl
COPY entrypoint.sh .
COPY default.conf.esh /etc/nginx/
ENV TZ="Europe/Moscow"
RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]