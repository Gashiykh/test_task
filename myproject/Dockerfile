FROM python:3.11-alpine

WORKDIR /app

RUN apk add --no-cache postgresql-client

COPY ../requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

COPY ../entrypoint.sh /app/entrypoint.sh

RUN chmod +x /app/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]
