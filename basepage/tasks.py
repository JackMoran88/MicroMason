from MicroMason.celery import app
from .service import mailer_send, mailer_html_send
import os
from django.template.loader import render_to_string
from django.conf import settings
from order.models import Order, OrderProduct


def commit_email():
    os.seteuid(0)
    os.system("python manage.py send_mail")


@app.task
def send_email(subject, body, recipients):
    mailer_send(subject, body, recipients)


@app.task
def send_beat_email():
    print('ОТПРАВЛЯЮ МЫЛО')
    commit_email()


def se_order(type, order, recipients):
    if type == 'create':
        print('EMAIL ORDER CREATE****')
        products = OrderProduct.objects.filter(order=order)
        print(products)


        msg_html = render_to_string('../templates/email/order/order_created.html',
                                    {
                                        'user_name': order.customer.get_full_name(),
                                        'order': order,
                                        'products': products,
                                        'settings': settings
                                    }
                                    )
        mailer_html_send(subject=f'Ваша заявка №{order.id} - принята', recipients=recipients, html=msg_html)

# Для переодических задач
# docker-compose run web celery -A MicroMason beat -l info
# Для обычных
# docker-compose run web celery -A MicroMason worker -l info
