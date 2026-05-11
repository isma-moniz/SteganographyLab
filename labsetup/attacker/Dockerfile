FROM python:3.14.4-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl \
    file \
	exiftool \
    xxd \
	bsdmainutils \
	less \
    && rm -rf /var/lib/apt/lists/*

RUN pip install pillow

COPY embed.py .
COPY duck.png .
COPY payload.sh .
