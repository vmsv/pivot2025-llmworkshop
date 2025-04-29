FROM python:3.12-alpine3.21


# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install dependencies
RUN apk update && apk add --no-cache gcc musl-dev libffi-dev curl zsh

WORKDIR /app
COPY requirements.txt ./

RUN pip install -r requirements.txt