FROM python:3.7

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get install -y libmagic-dev
RUN apt-get install -y cron
RUN apt install gettext -y

#ADD crontab /etc/crontab
RUN chmod 0644 /etc/crontab

WORKDIR /usr/src/micromason

COPY req.txt /usr/src/req.txt

RUN python -m pip install --upgrade pip

RUN pip install -r /usr/src/req.txt
RUN pip install django-novaposhta


COPY . /usr/src/micromason

#EXPOSE 8000

#CMD ["python", "manage.py", "migrate"]
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]