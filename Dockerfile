FROM python:3 as base

RUN pip install fastapi[all] alembic psycopg2-binary geoalchemy2 pytest

COPY . /app/.

WORKDIR /app

CMD ["bin/start"]