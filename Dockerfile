FROM ruby:latest

RUN gem install \
  github-pages \
  jekyll \
  jekyll-paginate \
  jekyll-seo-tag \
  kramdown \
  rouge

VOLUME /src

USER 1000:1000

WORKDIR /src
ENTRYPOINT ["jekyll", "serve"]
