# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from mis_template.utils.test.generic_test_case import GenericTestCase


class GenericServiceTest(GenericTestCase):
    logger = logging.getLogger(__name__)

    def setUp(self):
        self.logger.debug('#### setUp START ####')

        self.model_name = ''
        self.service = None

        self.invalid_field_value = None
        self.valid_field_name = None
        self.invalid_field_value = None
        self.non_existent_field_value = None
        self.valid_field_value = None

        self.logger.debug('#### setUp END ####')

    def get_all(self):
        self.logger.debug('#### TEST service get all %s START ####' % self.model_name)

        # get_all
        object_list = self.service.get_all()
        self.assertGreater(len(object_list), 0)

        self.logger.debug('#### TEST service get all %s END ####' % self.model_name)

    def get_by_pk(self):
        self.logger.debug('#### TEST service get %s by pk START ####' % self.model_name)

        # Should raise Exception if pk is None
        self.assertRaises(Exception, self.service.get_by_pk, None)

        # Should raise Exception if pk is invalid
        self.assertRaises(Exception, self.service.get_by_pk, self.invalid_id)

        # Should raise Exception if pk is invalid
        self.assertRaises(Exception, self.service.get_by_pk, self.non_existent_id)

        # get document with pk 1
        object_element = self.service.get_by_pk(self.valid_id)
        self.assertTrue(object_element)
        self.assertTrue(object_element.id)
        self.assertEqual(object_element.id, self.valid_id)

        self.logger.debug('#### TEST service get %s by pk END ####' % self.model_name)

    def get_by_field(self, field_name):
        self.logger.debug('#### TEST service get %s by %s START ####' % (self.model_name, field_name))

        # Should raise Exception if pk is None
        self.assertRaises(Exception, self.service.get_by_field, None, None)

        # Should raise Exception if pk is invalid
        if self.invalid_field_value:
            self.assertRaises(Exception, self.service.get_by_field, self.invalid_field_value, self.invalid_field_value)
            self.assertRaises(Exception, self.service.get_by_field, self.valid_field_name, self.invalid_field_value)

        # Should raise Exception if pk is invalid
        self.assertRaises(Exception, self.service.get_by_field, self.invalid_field_value, self.non_existent_field_value)
        self.assertRaises(Exception, self.service.get_by_field, self.valid_field_name, self.non_existent_field_value)

        # get document with pk 1
        object_element = self.service.get_by_field(self.valid_field_name, self.valid_field_value)
        self.assertTrue(object_element)
        self.assertTrue(getattr(object_element, self.valid_field_name))
        self.assertEqual(getattr(object_element, self.valid_field_name), self.valid_field_value)

        self.logger.debug('#### TEST service get %s by pk END ####' % self.model_name)
