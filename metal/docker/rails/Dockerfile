FROM ruby:2.5-alpine

RUN set -x \
    && apk --update add --virtual build-tools build-base ruby-dev \
    && apk --update add nodejs \
    && apk --update add vim

COPY ./aliases.sh /etc/profile.d
RUN source /etc/profile.d/aliases.sh

WORKDIR /app

EXPOSE 8000
