FROM python:3-alpine3.15

ENV LOG_LEVEL="INFO"

WORKDIR /app

COPY . .

EXPOSE 25565

ENTRYPOINT ["/usr/local/bin/python", "__main__.py"]
