from sendgrid.helpers.mail import (Mail, Email, Personalization)
from django.conf import settings
from celery import shared_task
import sendgrid


@shared_task
def send_email_task(template, data, to):
    sg = sendgrid.SendGridAPIClient(settings.SENDGRID_API_KEY)
    mail = Mail()
    mail.template_id = template
    mail.from_email = Email(settings.DEFAULT_FROM_EMAIL)
    personalization = Personalization()
    personalization.add_to(Email(to))
    personalization.dynamic_template_data = data
    mail.add_personalization(personalization)
    sg.client.mail.send.post(request_body=mail.get())
