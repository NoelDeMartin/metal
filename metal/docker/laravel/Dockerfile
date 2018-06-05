FROM php:7.2-alpine

RUN set -x \
    && apk --update add vim \
    && apk --update add --virtual node nodejs nodejs-npm \
    && php -r "readfile('http://getcomposer.org/installer');" | php -- --install-dir=/usr/bin/ --filename=composer \
    # TODO only do this if mongo is necessary
    && apk --update add --virtual build-tools build-base autoconf \
    && pecl install mongodb \
    && docker-php-ext-enable mongodb \
    # TODO only do this if mysql is necessary
    && docker-php-ext-install pdo pdo_mysql

COPY ./aliases.sh /etc/profile.d
RUN source /etc/profile.d/aliases.sh

WORKDIR /app

EXPOSE 8000
