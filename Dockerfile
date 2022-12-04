FROM python:3.11-alpine

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN apk add --no-cache dumb-init \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["dumb-init", "sh", "start.sh"]
