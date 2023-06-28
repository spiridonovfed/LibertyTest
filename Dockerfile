FROM python:3.8

RUN apt-get update -y && \
    apt-get install -y apt-utils && \
    apt-get upgrade -y && \
    apt-get install -y locales && \
    apt-get dist-upgrade

ENV APP_HOME=/liberty_test_task
ENV PYTHONPATH=${PYTHONPATH}:/liberty_test_task

WORKDIR ${APP_HOME}
COPY . ${APP_HOME}
RUN test -f .env || cp .env.example .env

RUN cd liberty_test_task

RUN pip install -U pip
RUN pip install -r requirements.txt

EXPOSE 8000