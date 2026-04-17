# Build from repository root: docker build -f docker/backend/Dockerfile .
FROM public.ecr.aws/docker/library/python:3.12-alpine AS builder
WORKDIR /app
COPY app/requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM public.ecr.aws/docker/library/python:3.12-alpine
WORKDIR /app
RUN apk add --no-cache curl
COPY --from=builder /install /usr/local
COPY app/ .
ENV APP_VERSION=1.0.0 \
    APP_COLOR=green \
    APP_ENV=production \
    PORT=80
EXPOSE 80
CMD ["gunicorn", "--bind", "0.0.0.0:80", "--workers", "2", "--timeout", "30", "app:app"]
