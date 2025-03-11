FROM python:3.11-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN mkdir -p config.STATIC_ROOT && chmod -R 755 config.STATIC_ROOT

EXPOSE 8000

