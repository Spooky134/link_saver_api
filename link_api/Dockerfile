FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/

# healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ./pyproject.toml ./poetry.lock ./

RUN pip install --no-cache-dir poetry==2.3.1

RUN poetry config virtualenvs.create false  \
    && poetry install --no-interaction --no-ansi --without dev --no-root

COPY ./app/ .

CMD ["gunicorn", "main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000"]