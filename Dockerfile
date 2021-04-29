FROM ruby:latest

ADD Gemfile .
RUN bundle install

VOLUME /src

USER 1000:1000

WORKDIR /src
ENTRYPOINT ["jekyll", "serve"]
