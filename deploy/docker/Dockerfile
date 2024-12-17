FROM python:3.12-slim AS builder

RUN pip install --no-cache-dir poetry
COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt --output requirements.txt

FROM python:3.12-alpine
WORKDIR /app

COPY --from=builder requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
  pip install gunicorn uvicorn && \
  rm -rf /root/.cache/pip && \
  rm requirements.txt

COPY config.py ./
COPY app ./app

ENV PORT=8000
ENV WORKERS=4
EXPOSE $PORT

CMD gunicorn app.main:app_router -w $WORKERS -k uvicorn.workers.UvicornWorker -b 0.0.0.0:${PORT}