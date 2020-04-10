FROM python:3.7

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install Yarn & node
RUN apt-get -qq update && apt-get -qq install curl apt-transport-https && \
    curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - && \
    echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list && \
    curl -s https://deb.nodesource.com/gpgkey/nodesource.gpg.key | apt-key add - && \
    echo 'deb https://deb.nodesource.com/node_8.x jessie main' > /etc/apt/sources.list.d/nodesource.list

# Install dependencies
COPY system-requirements.txt package.json yarn.lock Pipfile Pipfile.lock /

RUN  \
    apt-get -qq update && \
    xargs apt-get -qq install < system-requirements.txt

RUN yarn install && pip install pipenv && pipenv install --system

# Set work directory
WORKDIR /app

# Copy project
COPY src .

# Prepare entry point
COPY entrypoint.sh /

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]