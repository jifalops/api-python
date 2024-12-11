FROM python:3.12-slim AS builder

RUN pip install --no-cache-dir poetry
COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt --output requirements.txt

FROM public.ecr.aws/lambda/python:3.12

COPY --from=builder requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
  pip install mangum awslambdaric && \
  rm -rf /root/.cache/pip && \
  rm requirements.txt

WORKDIR ${LAMBDA_TASK_ROOT}
COPY app/ app/
COPY config.py .

CMD ["app.main.lambda_handler"]