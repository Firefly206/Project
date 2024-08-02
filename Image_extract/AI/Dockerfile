FROM python:3.10-buster

EXPOSE 3003

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

WORKDIR /agm/src/ai

COPY . .

RUN set -eux; \
    apt-get update -y && \
    apt-get install -y build-essential cmake pkg-config libzbar-dev python3-opencv

RUN pip3 install -r requirements.txt

CMD ["gunicorn", "--bind", "0.0.0.0:3003", "main:app"]