FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /code

WORKDIR /code

RUN apt-get update && apt-get install -y build-essential cmake

COPY requirements.txt /code/

RUN pip install torch --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir --timeout 600 -r requirements.txt

COPY . /code/

