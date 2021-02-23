FROM python:3.7

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


WORKDIR /usr/src/micromason

COPY ./req.txt /usr/src/req.txt
RUN pip install -r /usr/src/req.txt


