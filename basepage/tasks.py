from MicroMason.celery import app
from .service import send
import os


def commit_email():
    os.seteuid(0)
    os.system("python manage.py send_mail")


@app.task
def send_email(subject, body, recipients):
    send(subject, body, recipients)


@app.task
def send_beat_email():
    print('ОТПРАВЛЯЮ МЫЛО')
    commit_email()


def se_order(type, order, recipients):
    if type == 'update':
        send_email('Ваш заказ был обновлен', f'Заказ #{order.id} был обновлен', recipients)


# Для переодических задач
# docker-compose run web celery -A MicroMason beat -l info
# Для обычных
# docker-compose run web celery -A MicroMason worker -l info
