FROM python:3.7.6-alpine3.10 as base



FROM base AS base-build

# # Install system dependencies.
RUN apk add --no-cache \
    gcc libc-dev make linux-headers musl-dev python-dev

RUN mkdir -p /opt/local

# Copy requirements and install.
COPY requirements.txt /tmp/
RUN pip install -U setuptools pip && pip install \
    --prefix=/opt/local \
    --disable-pip-version-check \
    --no-warn-script-location \
    -r /tmp/requirements.txt



FROM base AS final-build

# Install system dependencies.
RUN apk add --no-cache bash

# Copy requirements from builder image.
COPY --from=base-build /opt/local /opt/local

ENV APP_NAME=budget \
    APP_PATH=/app \
    PATH=/opt/local/bin:$PATH \
    PYTHONPATH=/opt/local/lib/python3.7/site-packages:/app/budget \
    PYTHONUNBUFFERED=1

WORKDIR $APP_PATH

# Copy application source.
COPY . $APP_PATH
