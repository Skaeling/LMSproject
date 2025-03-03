FROM python:3.11-slim

WORKDIR /

RUN apt-get update \
    && apt-get install -y gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /static


EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]