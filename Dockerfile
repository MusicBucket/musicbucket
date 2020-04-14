FROM python:3.8

# Set work directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install Yarn & node
RUN apt-get -qq update && apt-get -qq install curl apt-transport-https && \
    curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - && \
    echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list && \
    curl -s https://deb.nodesource.com/gpgkey/nodesource.gpg.key | apt-key add - && \
    echo 'deb https://deb.nodesource.com/node_8.x jessie main' > /etc/apt/sources.list.d/nodesource.list

COPY docker/locale.gen /etc/locale.gen
COPY system-requirements.txt /srv/system-requirements.txt
# Install system dependencies
RUN \
    apt-get -qq update && \
    xargs apt-get -qq install < /srv/system-requirements.txt

# Pipenv
COPY Pipfile* /srv/
RUN \
    pip install --upgrade pip && \
    pip install pipenv
WORKDIR /srv
RUN pipenv install --system --ignore-pipfile
# End Pipenv

# Yarn
WORKDIR /app
COPY package.json /node/package.json
RUN cd /node && yarn install && cd /app
# End Yarn

# Copy project
COPY src/ .
COPY docker/entrypoint.sh /entrypoint.sh
COPY docker/app.docker.ini /app/app.ini
COPY docker/app.docker.ini /srv/app.ini

RUN mkdir -p /app/main/static && cd /app/main/static/ && yarn install && cd /app

# Entrypoint
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
EXPOSE 8000 1337


