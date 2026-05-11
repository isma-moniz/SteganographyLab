FROM python:3.14.4-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
	curl \
	exiftool \
	file \
	xxd \
	&& rm -rf /var/lib/apt/lists/*

RUN pip install pillow

COPY extractor.py .
COPY imv_fake.sh .
