from io import BytesIO
from celery import task
import weasyprint
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from orders.models import Order

@task
def payment_completed(order_id):
    '''
    Task to send email notification when an order created successfully
    '''
    order = Order.objects.get(id=order_id)

    # create invoice e-mail
    subject = f'MERCURY - EE Invoice no. {order.id}'
    message = 'Please, find attached invoice for your recent purchase'
    email = EmailMessage(subject, message, 'admin@mercury.com', [order.email])
    
    # generate pdf
    html = render_to_string('orders/order/pdf.html', {'order': order})
    out = BytesIO()
    stylesheets = [weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')]
    weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)

    # attach pdf file
    email.attach(f'order_{order.id}.pdf', out.getvalue(), 'application/pdf')

    # send email
    email.send()
