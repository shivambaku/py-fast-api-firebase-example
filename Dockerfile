FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src/server ./server

EXPOSE ${PORT}

CMD exec uvicorn server.app:app --host 0.0.0.0 --port ${PORT} 
