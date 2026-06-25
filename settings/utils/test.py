# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import logging
from datetime import date

from django.core import serializers
from django.test import TestCase, Client


class InvalidObject(object):
    pass


class GenericTestCase(TestCase):
    logger = logging.getLogger(__name__)

    available_apps = ['django.contrib.admin', 'django.contrib.auth', 'django.contrib.contenttypes',
                      'django.contrib.sessions', 'django.contrib.messages', 'django.contrib.staticfiles', ]

    client = Client(enforce_csrf_checks=True)

    authorized_username = 'misuser'
    unauthorized_username = 'fake'
    authorized_user = None
    unauthorized_user = None

    admin_username = 'misuser'

    all_roles_list = []

    invalid_json = {'data': 'invalid'}
    invalid_id = 'xxxxx'
    non_existent_id = 999999

    valid_id = 1

    invalid_object = InvalidObject()

    today = date.today()

    field_required_text = 'This field is required.'
    field_length_exceeded_text = 'Ensure this value has at most %s characters (it has %s).'

    def model_to_request_json(self, model):
        self.logger.debug(model)
        serialized_model_json_list = json.loads(serializers.serialize('json', [model]))
        result_json = {}
        serialized_model_json = serialized_model_json_list[0]
        for key, value in serialized_model_json.items():
            if key == 'fields':
                result_json = value
        return result_json



