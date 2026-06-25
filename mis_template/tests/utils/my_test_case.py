# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import shutil

from mis_template.utils.test.generic_test_case import GenericTestCase


class MisTemplateTestCase(GenericTestCase):
    logger = logging.getLogger(__name__)

    def setUp(self):
        self.logger.debug('#### setUp START ####')
        self.logger.debug('#### setUp END ####')

    def cleanDirectory(self, dir_to_delete):
        try:
            shutil.rmtree(dir_to_delete, ignore_errors=True)
        except Exception as e:
            self.logger.error('Error removing directory: %s' % e)

    def check_mandatory_sidebar_menu_json(self, json):
        self.assertIsInstance(json, dict)
        self.assertTrue(json['id'])
        self.assertTrue(json['name'])

    def check_mandatory_feature_json(self, json):
        self.assertIsInstance(json, dict)
        self.assertTrue(json['id'])
        self.assertTrue(json['code'])

    def check_mandatory_label_json(self, json):
        self.assertIsInstance(json, dict)
        self.assertTrue(json['id'])
        self.assertTrue(json['code'])
