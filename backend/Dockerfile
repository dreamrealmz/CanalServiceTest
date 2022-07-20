# Dockerfile
# Pull base image
FROM python:3.9
# Set work directory
ENV APP_DIR=/usr/backend/django_app
WORKDIR $APP_DIR
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install -y libpq-dev gcc python3-dev libffi-dev libblas-dev liblapack-dev libatlas-base-dev gfortran postgresql postgresql-client


# Install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt $APP_DIR/requirements.txt
RUN pip install -r requirements.txt

# Copy project
COPY . $APP_DIR
