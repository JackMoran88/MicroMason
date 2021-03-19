from MicroMason.celery import app
from .service import mailer_send, mailer_html_send
import os
from django.template.loader import render_to_string
from django.conf import settings
from order.models import Order, OrderProduct
from _novaposhta.services import getStatusDocuments
from _novaposhta.models import Delivery


# def commit_email():
#     os.seteuid(0)
#     os.system("python manage.py send_mail")


@app.task
def send_email(subject, body, recipients):
    mailer_send(subject, body, recipients)


@app.task
def send_beat_email():
    print('ОТПРАВЛЯЮ МЫЛО')
    # commit_email()


def se_order(type, order, recipients):
    if type == 'create':
        print('EMAIL ORDER CREATE****')
        products = OrderProduct.objects.filter(order=order)
        print(products)

        msg_html = render_to_string('../templates/email/templates/order_created.html',
                                    {
                                        'user_name': order.address.get_name(),
                                        'order': order,
                                        'products': products,
                                        'settings': settings
                                    }
                                    )
        mailer_html_send(subject=f'Ваша заявка №{order.id} - принята', recipients=recipients, html=msg_html)


@app.task
def np_update_invoice():
    print('np_update_invoice')
    getStatusDocuments('20450357650983')
    Delivery.objects.filter(int_doc_number='20450357650983').update(status='TEST')

# Для переодических задач
# docker-compose run web celery -A MicroMason beat -l info
# Для обычных
# docker-compose run web celery -A MicroMason worker -l info
