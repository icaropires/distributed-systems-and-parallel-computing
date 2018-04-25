FROM python:3

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /home/repository/repository
WORKDIR /home/repository/repository	

ADD requirements.txt ..
RUN pip install -r ../requirements.txt
