# Use an official Python 3.11.8 runtime as the base image
FROM python:3.11.8-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the poetry files (pyproject.toml and poetry.lock) to the container
COPY pyproject.toml poetry.lock /app/

# Install poetry and project dependencies
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi

# Install Redis
RUN apt-get update && apt-get install -y redis-server

# Copy the rest of the application code to the container
COPY . /app/

# Command to start Redis and run Celery
CMD ["sh", "-c", "service redis-server start && celery -A nerfcfm.celery worker -l INFO"]

