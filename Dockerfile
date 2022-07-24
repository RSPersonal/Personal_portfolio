FROM python:3.9-buster

WORKDIR /code/

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt update \
    && apt install postgresql-client -y

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY docker-entrypoint.sh .
RUN sed -i 's/\r$//g' /code/docker-entrypoint.sh
RUN chmod +x /code/docker-entrypoint.sh

COPY . .

ENTRYPOINT ["/code/docker-entrypoint.sh"]