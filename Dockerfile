FROM python:3.11-slim as builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential libpq-dev

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install virtualenv && \
    virtualenv /env && \
    /env/bin/pip install -r requirements.txt

FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY --from=builder /env /env

COPY alembic ./alembic
COPY app ./app
COPY tests ./tests
COPY alembic.ini ./

ENV PATH="/env/bin:$PATH"

EXPOSE 8000

# RUN alembic upgrade head

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
