# ── Stage 1: build dependencies ──────────────────────────────────────────────
error
FROM public.ecr.aws/docker/library/python:3.12-alpine AS builder

WORKDIR /app
COPY app/requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ── Stage 2: runtime image ────────────────────────────────────────────────────
FROM public.ecr.aws/docker/library/python:3.12-alpine

WORKDIR /app

RUN apk add --no-cache curl

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy application source
COPY app/ .

ENV APP_VERSION=1.0.0 \
    APP_COLOR=green    \
    APP_ENV=production \
    PORT=80

EXPOSE 80

# Use gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:80", "--workers", "2", "--timeout", "30", "app:app"]
