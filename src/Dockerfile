FROM python:3.10.8-slim

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r /app/requirements.txt

EXPOSE 4200

CMD prefect config set PREFECT_API_URL=http://0.0.0.0:4200/api && prefect server start --host 0.0.0.0 --port 4200
