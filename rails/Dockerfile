FROM ruby:2.5-alpine

RUN apk --update add --virtual build-tools build-base ruby-dev
RUN apk --update add nodejs

WORKDIR /app

ADD . /app

RUN bundle install

EXPOSE 3000
