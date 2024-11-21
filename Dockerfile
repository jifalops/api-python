FROM python:3.12-slim as builder

RUN pip install poetry
COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt --with container --output requirements.txt

FROM python:3.12-slim
COPY --from=builder requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["gunicorn", "app.main:app_router", "-w", "4", "-k", "uvicorn.workers.UvicornWorker"]