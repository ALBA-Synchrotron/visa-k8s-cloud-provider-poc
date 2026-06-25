# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import logging
from datetime import date

from django.contrib.auth.models import User
from django.core import serializers
from django.test import TestCase, Client

from mis_template.utils import status


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

    app_admin_username = None
    app_manager_username = None
    app_user_username = None
    app_nonauthorized_username = 'nouser'

    all_roles_list = [app_admin_username, app_manager_username, app_user_username, app_nonauthorized_username]

    invalid_json = {'data': 'invalid'}
    invalid_id = 'xxxxx'
    non_existent_id = 999999

    valid_id = 1

    invalid_object = InvalidObject()

    today = date.today()

    field_required_text = 'This field is required.'
    field_length_exceeded_text = 'Ensure this value has at most %s characters (it has %s).'

    json_content_type = 'application/json'

    def get_or_create_user(self, username, password):
        try:
            user = User.objects.get(username=username)
        except Exception as e:
            self.logger.error(e)
            user = User.objects.create_user(username=username)
        user.set_password(password)
        user.save()
        return user

    def get_unauthorized_user(self):
        try:
            self.unauthorized_user = User.objects.get(username=self.unauthorized_username)
        except Exception as e:
            self.logger.error(e)
            self.unauthorized_user = User.objects.create_user(username=self.unauthorized_username)

    def login(self, username):
        self.logger.debug('#### Logging in as %s ####' % username)
        default_password = '12345'
        try:
            user = User.objects.get(username=username)
        except Exception as e:
            self.logger.error(e)
            user = User.objects.create_user(username=username)
        user.set_password(default_password)
        if username == self.admin_username:
            user.is_superuser = True
            user.is_staff = True
        user.save()
        result_login = self.client.login(username=username, password=default_password)
        self.assertTrue(result_login, 'Login incorrect for user %s' % username)

    def allowed_http_methods_testing(self, test_url, allowed_http_methods):
        self.logger.debug('#### START Testing allowed HTTP methods ####')
        self.logger.debug(test_url + " - " + str(allowed_http_methods))
        if test_url and isinstance(allowed_http_methods, list):
            if 'GET' not in allowed_http_methods:
                response = self.client.get(test_url)
                self.assertEqual(str(response.status_code), str(status.HTTP_405_METHOD_NOT_ALLOWED))
            if 'POST' not in allowed_http_methods:
                response = self.client.post(test_url)
                self.assertEqual(str(response.status_code), str(status.HTTP_405_METHOD_NOT_ALLOWED))
            if 'PUT' not in allowed_http_methods:
                response = self.client.put(test_url)
                self.assertEqual(str(response.status_code), str(status.HTTP_405_METHOD_NOT_ALLOWED))
            if 'DELETE' not in allowed_http_methods:
                response = self.client.delete(test_url)
                self.assertEqual(str(response.status_code), str(status.HTTP_405_METHOD_NOT_ALLOWED))
        self.logger.debug('#### END Testing allowed HTTP methods ####')

    def login_and_check_http_methods(self, username, test_url, allowed_http_methods):
        self.login(username)
        self.allowed_http_methods_testing(test_url, allowed_http_methods)

    def model_to_request_json(self, model):
        self.logger.debug(model)
        serialized_model_json_list = json.loads(serializers.serialize('json', [model]))
        result_json = {}
        serialized_model_json = serialized_model_json_list[0]
        for key, value in serialized_model_json.items():
            if key == 'fields':
                result_json = value
        return result_json

    @staticmethod
    def args_to_url(filter_args):
        arg_string = ''
        for idx, arg in enumerate(filter_args):
            if idx == 0:
                arg_string += '?'
            else:
                arg_string += '&'
            arg_string += '%s=%s' % (arg, filter_args[arg])
        return arg_string

    def logout(self):
        self.logger.debug('#### Logging out ####')
        self.client.logout()
        self.logger.debug('#### Logged out ####')

    def check_roles_method_request(self, url, method=None, data=None):
        if method is None or method == 'GET':
            self.logger.debug('#### Checking roles for GET method and url: %s ####' % url)
            return self.client.get(url)
        if method == 'POST':
            if data is not None:
                self.logger.debug('#### Checking roles for POST method and url: %s ####' % url)
                return self.client.post(url, data=data, content_type=self.json_content_type)
            else:
                self.logger.debug('#### Checking roles for POST method and url: %s ####' % url)
                return self.client.post(url)
        if method == 'PUT':
            self.logger.debug('#### Checking roles for PUT method and url: %s ####' % url)
            return self.client.put(url, data=data, content_type=self.json_content_type)
        if method == 'DELETE':
            self.logger.debug('#### Checking roles for DELETE method and url: %s ####' % url)
            return self.client.delete(url)
        if method == 'HEAD':
            self.logger.debug('#### Checking roles for HEAD method and url: %s ####' % url)
            return self.client.head(url)
        if method == 'OPTIONS':
            self.logger.debug('#### Checking roles for OPTIONS method and url: %s ####' % url)
            return self.client.options(url)
        if method == 'PATCH':
            self.logger.debug('#### Checking roles for PATCH method and url: %s ####' % url)
            return self.client.patch(url)

    def check_roles(self, usernames_list, url, method=None, data=None, cas_auth=True):
        self.logger.debug('#### Checking roles ####')

        self.logger.debug('#### Checking not logged user ####')
        self.logout()
        self.logger.debug('# TEST URL --> %s' % url)
        self.logger.debug('# TEST DATA --> %s' % data)
        response = None
        if method == 'GET':
            response = self.client.get(url)
        elif method == 'POST':
            response = self.client.post(url, data, format='json', content_type=self.json_content_type)
        elif method == 'PUT':
            response = self.client.put(url, data, format='json', content_type=self.json_content_type)
        elif method == 'DELETE':
            response = self.client.delete(url)
        if response:
            if cas_auth:
                self.logger.debug('Redirect to CAS')
                self.assertEqual(response.status_code, status.HTTP_302_FOUND)
            else:
                self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.get_unauthorized_user()

        all_roles = self.all_roles_list
        usernames_list.append(self.admin_username)
        self.logger.debug('ROLES: %s' % usernames_list)
        self.logger.debug("Checking response with valid roles")
        response = None
        for username in usernames_list:
            self.logger.debug('Checking response got with login %s with a valid role.' % username)
            self.login(username)
            response = self.check_roles_method_request(url, method, data)
            self.assertNotEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
            self.logout()

            if username in all_roles:
                all_roles.remove(username)
        valid_response = response

        self.logger.debug("Checking response with invalid roles")
        for invalid_role in all_roles:
            self.logger.debug('Checking response got with login %s as an invalid role.' % invalid_role)
            self.login(invalid_role)
            response = self.check_roles_method_request(url, method, data)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            self.logout()

        return valid_response

    @staticmethod
    def keep_json_keys(json_element={}, keys_to_keep_list=[]):
        result_json = {}
        for key in json_element.keys():
            if key in keys_to_keep_list:
                result_json[key] = json_element[key]
        return result_json

    @staticmethod
    def normalize_json_to_post(json_element={}):
        for key in json_element.keys():
            if json_element[key] == None:
                json_element[key] = ''
        return json_element

    def check_mandatory_response_error(self, response_json):
        self.assertIsInstance(response_json, dict, 'The response content should be a dict')
        self.assertTrue(response_json['error'], 'The error should not be null')
