from MicroMason.celery import app
from .service import mailer_send, mailer_html_send
import os
from django.template.loader import render_to_string
from django.conf import settings
from order.models import Order, OrderProduct
from _novaposhta.services import getStatusDocuments
from _novaposhta.models import Delivery



@app.task
def send_email(subject, body, recipients):
    mailer_send(subject, body, recipients)


@app.task
def send_beat_email():
    pass


def se_order(type, order, recipients):
    if type == 'create':
        products = OrderProduct.objects.filter(order=order)

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
    print('START np_update_invoice')
    deliveries = Delivery.objects.all()
    numbers = deliveries.values_list('int_doc_number', flat=True)
    documents = []
    for number in numbers:
        documents.append({'DocumentNumber': number, 'Phone': ''})

    result = getStatusDocuments(documents).json()
    if result['success'] == True:
        result = result['data']
        for item in result:
            Delivery.objects.filter(int_doc_number=item['Number']).update(status=item['Status'])

# Для переодических задач
# docker-compose run web celery -A MicroMason beat -l info
# Для обычных
# docker-compose run web celery -A MicroMason worker -l info
