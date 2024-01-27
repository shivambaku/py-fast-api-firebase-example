FROM python:3.11-slim

WORKDIR /app

RUN pip install pipenv

COPY Pipfile ./
COPY Pipfile.lock ./
RUN pipenv install --deploy --system --ignore-pipfile

COPY ./src/server ./server

EXPOSE ${PORT}

CMD exec uvicorn server.app:app --host 0.0.0.0 --port ${PORT} 


