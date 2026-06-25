# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import logging

from django.test.client import encode_multipart
from rest_framework import status

from mis_template.utils.test.generic_test_case import GenericTestCase
from mis_template.utils import labels


class GenericApiViewTest(GenericTestCase):
    logger = logging.getLogger(__name__)

    def setUp(self):
        self.model_name = ''
        self.reference_name = ''
        self.service_class = None
        self.serializer = None

        self.labels = labels

        self.is_sso_authenticated = False
        self.is_authenticated = False
        self.check_unauthorized_user = False
        self.check_authorized_user_list = []

        self.list_filter_list = [{}]

        self.model_class = None
        self.form_class = None
        self.has_files = False
        self.boundary_string = 'BoUnDaRyStRiNg'
        self.multipart_content_type = 'multipart/form-data; boundary=BoUnDaRyStRiNg'
        self.new_json_data = {}

        self.existing_object = 1
        self.not_existing_object = 9999

        self.template_directory_name = ''

        self.invalid_json_data = {'fake_attribute': 'fake_value'}
        self.create_validation = {}
        self.create_valid_minimum_json_data = {}
        self.create_valid_full_json_data = {}
        self.create_excluded_validation = []

        self.mandatory_field_list = []
        self.foreignkey_field_list = []

        self.update_validation = {}
        self.update_change_elements = []
        self.update_change_values = []
        self.update_excluded_validation = []

    def list(self):

        url = '/%s/all/' % self.reference_name

        if self.is_sso_authenticated:
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_302_FOUND)
            self.is_authenticated = True

        if self.is_authenticated:
            self.login_and_check_http_methods(self.authorized_username, url, ['GET', 'POST'])
        else:
            self.allowed_http_methods_testing(url, ['GET', 'POST'])

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        json_content = json.loads(response.content)
        self.assertIsInstance(json_content, list)
        self.assertGreater(len(json_content), 0)
        for json_element in json_content:
            eval('self.check_mandatory_%s_json(json_element)' % self.reference_name)

        if self.check_unauthorized_user:
            self.check_roles(self.check_authorized_user_list, url, 'GET', 'POST')

    def list_paginated(self):
        url = '/%s/' % self.reference_name

        if self.is_sso_authenticated:
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_302_FOUND)
            self.is_authenticated = True

        if self.is_authenticated:
            self.login_and_check_http_methods(self.authorized_username, url, ['GET', 'POST'])
        else:
            self.allowed_http_methods_testing(url, ['GET', 'POST'])

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        json_content = json.loads(response.content)

        self.assertTrue(json_content['count'])
        self.assertTrue(json_content['results'])
        self.assertIsInstance(json_content['results'], list)
        self.assertGreater(len(json_content['results']), 0)
        for json_element in json_content['results']:
            eval('self.check_mandatory_%s_json(json_element)' % self.reference_name)
        if self.check_unauthorized_user:
            self.check_roles(self.check_authorized_user_list, url, 'GET')

    def detail(self):
        root_url = '/%s/%s/'

        url = root_url % (self.reference_name, self.existing_object)

        if self.is_sso_authenticated:
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_302_FOUND)
            self.is_authenticated = True

        if self.is_authenticated:
            self.login_and_check_http_methods(self.authorized_username, url, ['GET'])
        else:
            self.allowed_http_methods_testing(url, ['GET'])

        # Should return status 404 for not existent object
        url = root_url % (self.reference_name, self.not_existing_object)
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Should return status 200 if everything goes fine
        url = root_url % (self.reference_name, self.existing_object)
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        json_content = json.loads(response.content)
        
        self.assertIsInstance(json_content, dict)
        eval('self.check_mandatory_%s_json(json_content)' % self.reference_name)

        if self.check_unauthorized_user:
            self.check_roles(self.check_authorized_user_list, url, 'GET')

        

    def new(self):
        

        url = '/%s/add/' % self.reference_name
        if self.is_sso_authenticated:
            
            response = self.client.get(url)
            
            self.assertEqual(response.status_code, status.HTTP_302_FOUND)
            self.is_authenticated = True

        if self.is_authenticated:
            self.login_and_check_http_methods(self.authorized_username, url, ['POST'])
        else:
            self.allowed_http_methods_testing(url, ['POST'])

        count = self.model_class.objects.count()

        # Test without data
        
        if self.has_files:
            response = self.client.post(url, {}, format='multipart')
        else:
            response = self.client.post(url, {}, format='json', content_type=labels.TEST_CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        json_content = json.loads(response.content)
        
        self.check_mandatory_response_error(json_content)

        # Test with invalid data
        
        json_data = self.invalid_json_data
        
        if self.has_files:
            response = self.client.post(url, json_data, format='multipart')
        else:
            response = self.client.post(url, json_data, format='json', content_type=labels.TEST_CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        json_content = json.loads(response.content)
        
        self.check_mandatory_response_error(json_content)

        for mandatory_field_name in self.mandatory_field_list:
            json_data = self.create_validation.copy()
            self.create_check_mandatory_fields(url, json_data, mandatory_field_name)

        # Add with minimum data
        
        json_data = self.create_valid_minimum_json_data
        
        if self.has_files:
            response = self.client.post(url, json_data, format='multipart')
        else:
            response = self.client.post(url, json_data, format='json', content_type=labels.TEST_CONTENT_TYPE)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        json_content = json.loads(response.content)
        
        eval('self.check_mandatory_%s_json(json_content)' % self.reference_name)

        # Checking if the register was created
        new_count = self.model_class.objects.count()
        self.assertEqual(new_count, (count + 1))
        count = new_count

        # Add with full data
        
        json_data = self.create_valid_full_json_data
        
        if self.has_files:
            response = self.client.post(url, json_data, format='multipart')
        else:
            response = self.client.post(url, json_data, format='json', content_type=labels.TEST_CONTENT_TYPE)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        json_content = json.loads(response.content)
        
        eval('self.check_mandatory_%s_json(json_content)' % self.reference_name)

        # Checking if the register was created
        new_count = self.model_class.objects.count()
        self.assertEqual(new_count, (count + 1))

        if self.check_unauthorized_user:
            self.check_roles(self.check_authorized_user_list, url, 'POST')

        

    def create_check_mandatory_fields(self, url, json_data, mandatory_field_name):
        json_data[mandatory_field_name] = ''
        if self.has_files:
            response = self.client.post(url, json_data, format='multipart')
        else:
            response = self.client.post(url, json_data, format='json', content_type=labels.TEST_CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        json_content = json.loads(response.content)
        
        self.check_mandatory_response_error(json_content)

    def update(self):
        
        
        root_url = '/%s/%s/update/'

        url = root_url % (self.reference_name, self.existing_object)
        if self.is_sso_authenticated:
            
            response = self.client.get(url)
            
            self.assertEqual(response.status_code, status.HTTP_302_FOUND)
            self.is_authenticated = True

        if self.is_authenticated:
            self.login_and_check_http_methods(self.authorized_username, url, ['PUT'])
        else:
            self.allowed_http_methods_testing(url, ['PUT'])

        count = self.model_class.objects.count()

        # Test without id
        url = root_url % (self.reference_name, '')
        
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Should return status 404 for not existent object
        url = root_url % (self.reference_name, self.not_existing_object)
        
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        json_content = json.loads(response.content)
        
        self.check_mandatory_response_error(json_content)

        # Test without data
        url = root_url % (self.reference_name, self.existing_object)
        
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        json_content = json.loads(response.content)
        
        self.check_mandatory_response_error(json_content)

        url = root_url % (self.reference_name, self.existing_object)
        for mandatory_field_name in self.mandatory_field_list:
            element = self.service_class.get_by_pk(self.existing_object)
            serializer = self.serializer(element)
            json_data = serializer.data
            self.update_check_mandatory_fields(url, json_data, mandatory_field_name)

        # Change data
        url = root_url % (self.reference_name, self.existing_object)
        
        if len(self.update_change_elements) == len(self.update_change_values) and len(self.update_change_elements) > 1:
            for index, name in enumerate(self.update_change_elements):
                element = self.service_class.get_by_pk(self.existing_object)
                serializer = self.serializer(element)
                json_data = serializer.data
                self.assertNotEqual(json_data[name], self.update_change_values[index])

                json_data[name] = self.update_change_values[index]
                
                if self.has_files:
                    response = self.client.put(url, encode_multipart(self.boundary_string, json_data),
                                               content_type=self.multipart_content_type)
                else:
                    response = self.client.post(url, json_data, format='json', content_type=labels.TEST_CONTENT_TYPE)
                self.assertEqual(response.status_code, status.HTTP_200_OK)

                json_content = json.loads(response.content)
                
                eval('self.check_mandatory_%s_json(json_content)' % self.reference_name)
                element = self.service_class.get_by_pk(self.existing_object)
                serializer = self.serializer(element)
                json_data = serializer.data
                self.assertEqual(json_data[name], self.update_change_values[index])

        if self.check_unauthorized_user:
            self.check_roles(self.check_authorized_user_list, url, 'POST')

        

    def update_check_mandatory_fields(self, url, json_data, mandatory_field_name):
        json_data[mandatory_field_name] = ''
        if self.has_files:
            response = self.client.put(url, encode_multipart(self.boundary_string, json_data),
                                       content_type=self.multipart_content_type)
        else:
            response = self.client.put(url, json_data, format='json', content_type=labels.TEST_CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        json_content = json.loads(response.content)
        
        self.check_mandatory_response_error(json_content)

    def delete(self):
        

        root_url = '/%s/%s/delete/'
        
        url = root_url % (self.reference_name, self.existing_object)
        if self.is_sso_authenticated:
            
            response = self.client.get(url)
            
            self.assertEqual(response.status_code, status.HTTP_302_FOUND)
            self.is_authenticated = True

        if self.is_authenticated:
            self.login_and_check_http_methods(self.authorized_username, url, ['DELETE'])
        else:
            self.allowed_http_methods_testing(url, ['DELETE'])

        # Test without id
        url = root_url % (self.reference_name, '')
        
        response = self.client.delete(url, format='json', content_type=labels.TEST_CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Test with invalid id
        url = root_url % (self.reference_name, self.invalid_id)
        
        response = self.client.delete(url, format='json', content_type=labels.TEST_CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Test with non existent id
        url = root_url % (self.reference_name, self.not_existing_object)
        
        response = self.client.delete(url, format='json', content_type=labels.TEST_CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        json_content = json.loads(response.content)
        
        self.check_mandatory_response_error(json_content)

        # Getting initial register number
        count = self.model_class.objects.count()

        url = root_url % (self.reference_name, self.existing_object)
        
        response = self.client.delete(url, format='json', content_type=labels.TEST_CONTENT_TYPE)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Checking if the register was deleted
        new_count = self.model_class.objects.count()
        self.assertEqual(new_count, (count - 1))

        if self.check_unauthorized_user:
            self.check_roles(self.check_authorized_user_list, url, 'DELETE')

        
