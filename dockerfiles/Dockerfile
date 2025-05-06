FROM python:3.12-slim


# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install dependencies
#RUN apk update && apk add --no-cache gcc musl-dev libffi-dev curl zsh
RUN apt update && apt install -y gcc curl zsh python3-pip

WORKDIR /app
COPY requirements.txt ./

RUN pip3 install -r requirements.txt
