# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from mis_template.utils.test.generic_test_case import GenericTestCase

logger = logging.getLogger(__name__)


class GenericFormTestCase(GenericTestCase):
    logger = logging.getLogger(__name__)

    def setUp(self):
        self.logger.debug('#### setUp START ####')

        self.model_class = None
        self.form_class = None
        self.model_name = ''
        self.invalid_json = {'invalid_field': 'invalid_data'}
        self.valid_json = {}
        self.create_json = {}

        self.logger.debug('#### setUp END ####')

    def empty(self):
        self.logger.debug('#### TEST form empty %s model START ####' % self.model_name)
        data = {}
        form = self.form_class(data=data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.logger.debug('#### TEST form empty %s model END ####' % self.model_name)

    def invalid(self):
        self.logger.debug('#### TEST form invalid %s model START ####' % self.model_name)
        form = self.form_class(data=self.invalid_json)
        self.assertFalse(form.is_valid())
        self.logger.debug('Form errors: %s' % form.errors)
        self.logger.debug('#### TEST form invalid %s model END ####' % self.model_name)

    def valid(self):
        self.logger.debug('#### TEST form valid %s model START ####' % self.model_name)
        self.logger.debug('self.valid_json: %s' % self.valid_json)
        form = self.form_class(data=self.valid_json)
        try:
            self.logger.debug('Form errors: %s' % form.errors)
        except Exception as e:
            self.logger.warning(e)
        self.assertTrue(form.is_valid())
        try:
            self.logger.debug('Form errors: %s' % form.errors)
        except Exception as e:
            self.logger.warning(e)
        self.assertFalse(form.errors)
        self.logger.debug('#### TEST form valid %s model END ####' % self.model_name)

    def create(self):
        self.logger.debug('#### TEST form create %s model START ####' % self.model_name)
        form = self.form_class(data=self.create_json)
        self.logger.debug('Form errors: %s' % form.errors)
        self.assertTrue(form.is_valid())
        self.logger.debug('Form errors: %s' % form.errors)
        self.assertFalse(form.errors)
        if form.is_valid():
            element = form.save()
            self.assertTrue(element.id)
        self.logger.debug('#### TEST form create %s model END ####' % self.model_name)


