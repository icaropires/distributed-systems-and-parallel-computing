FROM python:3

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /home/slave/slave
WORKDIR /home/slave/slave

ADD requirements.txt ..
RUN pip install -r ../requirements.txt
