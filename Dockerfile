FROM ruby:latest

RUN gem install \
  github-pages \
  jekyll \
  jekyll-paginate \
  jekyll-seo-tag \
  kramdown \
  rouge

VOLUME /src

WORKDIR /src
COPY . .
ENTRYPOINT ["jekyll", "serve"]
