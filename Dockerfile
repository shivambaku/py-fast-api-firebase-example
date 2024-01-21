FROM python:3.11-slim

WORKDIR /server

RUN pip install pipenv

COPY Pipfile ./
COPY Pipfile.lock ./
RUN pipenv install --deploy --system --ignore-pipfile

COPY . .

ENV PORT 8000

EXPOSE ${PORT}

CMD exec uvicorn server.app:app --host 0.0.0.0 --port ${PORT} 
