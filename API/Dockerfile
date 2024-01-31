FROM python:3.9.0-slim

WORKDIR /api

COPY ./requirements.txt /api/requirements.txt

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r /api/requirements.txt

COPY ./lib /api/lib
COPY main.py /api/main.py
COPY app_config.py /api/app_config.py

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
