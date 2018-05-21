FROM php:7.2-alpine

RUN apk --update add nodejs
RUN apk --update add vim
RUN php -r "readfile('http://getcomposer.org/installer');" | php -- --install-dir=/usr/bin/ --filename=composer

COPY ./aliases.sh /etc/profile.d
RUN source /etc/profile.d/aliases.sh

WORKDIR /app

EXPOSE 8000
