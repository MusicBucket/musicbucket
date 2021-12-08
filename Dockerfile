FROM python:3.10

# Set work directory
WORKDIR /app

ARG RQWORKER
ENV RQWORKER $RQWORKER

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# Install Yarn & node
RUN apt-get -qq update && apt-get -qq install curl apt-transport-https && \
    curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - && \
    echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list

RUN curl -fsSL https://deb.nodesource.com/setup_17.x | bash -

COPY docker/locale.gen /etc/locale.gen
COPY system-requirements.txt /srv/system-requirements.txt
# Install system dependencies
RUN \
    apt-get -qq update && \
    xargs apt-get -qq install < /srv/system-requirements.txt

# Poetry
COPY pyproject.toml* /srv/
RUN \
    pip install --upgrade pip && \
    pip install poetry
WORKDIR /srv
RUN poetry config virtualenvs.create false && \
    poetry install --no-dev
# End Poetry

# Yarn
WORKDIR /app
COPY package.json /node/package.json
RUN cd /node && yarn install && cd /app
# End Yarn

# Run the command on container startup
CMD cron && tail -f /var/log/cron.log

# Copy project
COPY src/ .
COPY docker/entrypoint.sh /entrypoint.sh
COPY docker/app.docker.ini /srv/app.ini
RUN cp /srv/app.ini /app/app.ini

RUN mkdir -p /app/main/static && cd /app/main/static/ && yarn install && cd /app

# Entrypoint
RUN chmod +x /entrypoint.sh
#ENTRYPOINT ["/entrypoint.sh"]
ENTRYPOINT /entrypoint.sh $RQWORKER

EXPOSE 8000

ENV STATIC_ROOT=/data/static

RUN mkdir -p /data/static && mkdir -p /data/media && \
    echo "Compiling messages..." && \
    CACHE_TYPE=dummy SECRET_KEY=musicbucket python manage.py compilemessages && \
    echo "Compressing..." && \
    CACHE_TYPE=dummy SECRET_KEY=musicbucket python manage.py compress --traceback --force && \
    echo "Collecting statics..." && \
    CACHE_TYPE=dummy SECRET_KEY=musicbucket python manage.py collectstatic --noinput --traceback -v 0 && \
    chmod -R 777 /data/

VOLUME /data/static
