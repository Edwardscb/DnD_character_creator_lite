FROM python:3.8.1-alpine
RUN apk update \
    && apk add libpq postgresql-dev \
    && apk add build-base \
    && apk add libffi-dev
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /app
CMD ["gunicorn", "-b", "0.0.0.0:8080", "--workers", "3", "app:app"]