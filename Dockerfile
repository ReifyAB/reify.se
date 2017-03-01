FROM ubuntu:xenial-20170214

RUN apt-get update \
    && apt-get -y install build-essential zlib1g-dev ruby-dev ruby nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/

RUN gem install github-pages -v 124

VOLUME /site

EXPOSE 4000

WORKDIR /site
ENTRYPOINT ["jekyll"]
