# Dockerfile minimal pour la V1
FROM python:3.11-slim

WORKDIR /app

COPY server.py .

RUN pip install flask

EXPOSE 5000

CMD ["python", "server.py"]
