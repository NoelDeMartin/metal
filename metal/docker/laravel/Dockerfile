FROM php:7.2-alpine

RUN set -x \
    && apk --update add vim \
    && apk --update add --virtual node nodejs nodejs-npm \
    && php -r "readfile('http://getcomposer.org/installer');" | php -- --install-dir=/usr/bin/ --filename=composer \
    # TODO optional mongo
    && apk --update add --virtual build-tools build-base autoconf \
    && pecl install mongodb \
    && docker-php-ext-enable mongodb \
    # TODO optional mysql
    && docker-php-ext-install pdo pdo_mysql \
    # TODO optional image extensions
    && apk --update add --virtual gd-libs freetype-dev libjpeg-turbo-dev libpng-dev \
    && docker-php-ext-configure gd --with-freetype-dir=/usr/include/ --with-jpeg-dir=/usr/include/ \
    && docker-php-ext-install gd \
    && docker-php-ext-install exif \
    # TODO optional mcrypt
    && apk add libmcrypt-dev \
    && pecl install mcrypt-1.0.1 \
    && docker-php-ext-enable mcrypt \
    && rm /var/cache/apk/* \
    # TODO optional xDebug
    && pecl install xdebug

COPY ./php.ini /usr/local/etc/php/conf.d
COPY ./aliases.sh /etc/profile.d
RUN source /etc/profile.d/aliases.sh

WORKDIR /app

EXPOSE 8000
