# Build from repository root: docker build -f docker/frontend/Dockerfile .
FROM public.ecr.aws/docker/library/nginx:alpine
COPY docker/frontend/nginx.conf /etc/nginx/conf.d/default.conf
COPY docker/frontend/html /usr/share/nginx/html
EXPOSE 80
