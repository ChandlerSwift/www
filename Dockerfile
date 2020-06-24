FROM ruby:latest

RUN gem install \
  github-pages \
  jekyll \
  jekyll-redirect-from \
  kramdown \
  rdiscount \
  rouge

VOLUME /src

WORKDIR /src
COPY . .
ENTRYPOINT ["jekyll", "serve"]
