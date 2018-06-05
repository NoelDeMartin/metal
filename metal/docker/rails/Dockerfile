FROM ruby:2.5-alpine

RUN set -x \
    && apk --update add vim \
    && apk --update add --virtual node nodejs nodejs-npm \
    && apk --update add --virtual build-tools build-base ruby-dev

COPY ./aliases.sh /etc/profile.d
RUN source /etc/profile.d/aliases.sh

WORKDIR /app

EXPOSE 8000
