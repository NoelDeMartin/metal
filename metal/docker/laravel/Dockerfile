FROM php:7.2-alpine

RUN set -x \
    && apk --update add nodejs \
    && apk --update add vim \
    && php -r "readfile('http://getcomposer.org/installer');" | php -- --install-dir=/usr/bin/ --filename=composer \
    # TODO only do this if mongo is necessary
    && apk --update add build-base \
    && apk --update add autoconf \
    && pecl install mongodb \
    && docker-php-ext-enable mongodb

COPY ./aliases.sh /etc/profile.d
RUN source /etc/profile.d/aliases.sh

WORKDIR /app

EXPOSE 8000
