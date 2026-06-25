# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from mis_template.utils.test.generic_test_case import GenericTestCase

logger = logging.getLogger(__name__)


class GenericModelTestCase(GenericTestCase):
    logger = logging.getLogger(__name__)

    def setUp(self):
        self.logger.debug('#### setUp START ####')

        self.model_class = None
        self.model_name = ''
        self.mandatory_fields_json = {}
        self.all_fields_json = {}

        self.existing_element_id = 1
        self.update_json = {}

        self.logger.debug('#### setUp END ####')

    def create(self):
        self.logger.debug('#### TEST create %s model START ####' % self.model_name)

        # Create an object with None data
        json_data = None
        self.assertRaises(Exception, self.model_class.objects.create, kwargs=json_data)

        # Create an object with empty fields
        json_data = {}
        self.assertRaises(Exception, self.model_class.objects.create, kwargs=json_data)

        count = self.model_class.objects.count()

        # Create an object with mandatory fields
        object_element = self.model_class.objects.create(**self.mandatory_fields_json)
        self.assertTrue(isinstance(object_element, self.model_class))
        for key in self.mandatory_fields_json.keys():
            eval('self.assertEqual(object_element.%s, self.mandatory_fields_json[\'%s\'])' % (key, key))

        new_count = self.model_class.objects.count()
        self.assertEqual(new_count, count + 1)
        count = self.model_class.objects.count()

        # Create an object with mandatory fields
        object_element = self.model_class.objects.create(**self.all_fields_json)
        self.assertTrue(isinstance(object_element, self.model_class))
        for key in self.all_fields_json.keys():
            eval('self.assertEqual(object_element.%s, self.all_fields_json[\'%s\'])' % (key, key))

        new_count = self.model_class.objects.count()
        self.assertEqual(new_count, count + 1)

        self.logger.debug('#### TEST create %s model END ####' % self.model_name)

    def update(self):
        self.logger.debug('#### TEST update %s model START ####' % self.model_name)

        count = self.model_class.objects.count()

        object_element = self.model_class.objects.get(pk=self.existing_element_id)
        for key in self.update_json.keys():
            setattr(object_element, key, self.update_json[key])
        object_element.save()
        self.assertTrue(isinstance(object_element, self.model_class))
        for key in self.update_json.keys():
            eval('self.assertEqual(object_element.%s, self.update_json[\'%s\'])' % (key, key))

        new_count = self.model_class.objects.count()
        self.assertEqual(new_count, count)

        self.logger.debug('#### TEST update %s model END ####' % self.model_name)
