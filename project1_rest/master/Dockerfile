FROM python:3

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /home/master/master
WORKDIR /home/master/master

ADD requirements.txt ..
RUN pip install -r ../requirements.txt
