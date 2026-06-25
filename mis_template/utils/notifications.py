# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
from datetime import datetime
from html.parser import HTMLParser

import requests
from django.conf import settings
from django.core.mail import EmailMessage
from django.template import loader
from icalendar import Calendar, Event, vCalAddress
from requests.auth import HTTPBasicAuth

from mis_template.services.feature import FeatureService
from settings import labels

logger = logging.getLogger(__name__)


class NotificationUtils:
    """
    Notification interface
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    @staticmethod
    def send_generic(email_to_list=[], email_cc_list=[], email_bcc_list=[], subject='', summary='', content=None,
                     private=False, attachment=None, attachment_mime=None, attachment_filename=None,
                     web_push_dict=None):
        if hasattr(settings, 'EMAIL_NOTIFICATIONS') and settings.EMAIL_NOTIFICATIONS:
            environment = settings.DJANGO_ENV if settings.DJANGO_ENV != 'PROD' else ''

            if not private:
                email_cc_list.append(settings.EMAIL_MIS_TRACK)

            template_notification = loader.get_template('mis_template/notification.html')
            template_notification_summary = loader.get_template('mis_template/notification_summary.html')

            template_notification_summary_context = {'summary': summary}

            notification_body = template_notification_summary.render(template_notification_summary_context)
            if content:
                notification_body += content

            template_notification_context = {'app_name': settings.APP_NAME, 'environment': environment,
                                             'notification_body': notification_body, 'year': datetime.now().year,
                                             'footer_email': settings.FOOTER_EMAIL}

            html_parser = HTMLParser()
            html_message = template_notification.render(template_notification_context)
            html_message = html_parser.unescape(html_message)

            try:
                if settings.DJANGO_ENV != 'PROD':
                    html_message = labels.NOTIFICATION_NOT_PROD_MESSAGE % (
                        html_message, email_to_list, email_cc_list, email_bcc_list, subject)
                    email_to_list = [settings.EMAIL_MIS_TRACK]
                    subject = labels.NOTIFICATION_SUBJECT_PREFIX % (settings.DJANGO_ENV, subject)
                    email_cc_list = []
                    email_bcc_list = []

                email = EmailMessage(subject=subject, body='', from_email=settings.REPORTING_EMAIL, to=email_to_list,
                                     cc=email_cc_list, bcc=email_bcc_list)

                if html_message:
                    email.attach(content=html_message, mimetype='text/html')
                if attachment and attachment_filename and attachment_mime:
                    email.attach(filename=attachment_filename, content=attachment, mimetype=attachment_mime)

                email.send()

                if web_push_dict:
                    NotificationUtils().send_web_notification(**web_push_dict)
            except Exception as e:
                logger.error('ERROR Sending notification: %s' % e)
        else:
            logger.debug('Notification flag disabled')
            logger.debug('Email to %s not sent' % email_to_list)

    def send_web_notification(self, subject, body, recipients, notification_code, redis_suffix, open_url='',
                              cc_list=None, no_html_body=None):
        """
        Send a web-push notification to a user

        @param subject: Short text to summarize the notification (ie.: Absence Confirmation)
        @param body: The body of the notification (ie.: Your absence has been approved. You have...)
        @param recipients: Username list of the notification recipient
        @param notification_code: Short code to identify the nature/category of the notification
        @param redis_suffix: String to identify the notification inside the category, appended to the identifier
        @param open_url: URL the user can consult on opening the notification
        @param cc_list: Username list of people who is in copy of the notification
        @param no_html_body: The body of the notification without html content to prevent push notification from failing
        """

        if not FeatureService().is_feature_enabled(settings.WEB_NOTIFICATIONS_FEATURE_CODE):
            self.logger.warning('Web-push is not enabled, will not send anything')
            return

        self.logger.info('Sending web-push notification')
        timestamp_created = datetime.now()
        notification_data = {'recipients': recipients, 'subject': subject, 'body': body, 'code': notification_code,
                             'created': timestamp_created.isoformat(), 'read': False, 'open_url': open_url,
                             'key_value': '%s:%s:%s' % (
                             settings.WEB_NOTIFICATIONS_CODE_SERVICE, notification_code.lower(), redis_suffix)}

        if cc_list:
            notification_data['cc'] = cc_list
        if no_html_body:
            notification_data['no_html_body'] = no_html_body

        self.logger.debug('Payload: %s' % notification_data)
        url = '%s/push_notification/new/' % settings.WEB_NOTIFICATIONS_BASE_URL
        self.logger.debug('URL: %s' % url)
        response = requests.post(url=url, json=notification_data,
                                 auth=HTTPBasicAuth(settings.WEB_NOTIFICATIONS_USERNAME,
                                                    settings.WEB_NOTIFICATIONS_PASSWORD))
        if response.ok:
            self.logger.info('Web-push notification successfully sent')
        else:
            self.logger.error('Error sending web-push notification: %s' % response.json())

    @staticmethod
    def generate_appointment_attachment(appointment):
        cal = Calendar()
        event = Event()
        event.add('dtstamp', datetime.now())

        if appointment and appointment.person and appointment.person.username:
            person_email = appointment.person.username + settings.EMAIL_DOMAIN
            organizer = vCalAddress('MAILTO:%s' % person_email)
            event.add('organizer', organizer)
        if appointment and appointment.start_date:
            if isinstance(appointment.start_date, str):
                start_date = datetime.strptime(appointment.start_date, '%Y-%m-%dT%H:%M%z')
            else:
                start_date = appointment.start_date
            event.add('dtstart', start_date)
        if appointment and appointment.end_date:
            if isinstance(appointment.end_date, str):
                end_date = datetime.strptime(appointment.end_date, '%Y-%m-%dT%H:%M%z')
            else:
                end_date = appointment.end_date
            event.add('dtend', end_date)
        if appointment and appointment.event and appointment.event.name:
            event.add('summary', appointment.event.name)

        cal.add_component(event)
        return cal.to_ical()
