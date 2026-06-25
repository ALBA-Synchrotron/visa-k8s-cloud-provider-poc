# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from object_template.services.my_object_name import MyObjectNameService
from object_template.tests.utils.generic_service_test_case import MyGenericServiceTest


class MyObjectNameServiceTest(MyGenericServiceTest):
    fixtures = ['my_object_name.json']

    def setUp(self):
        self.logger.debug('#### setUp START ####')
        super(MyObjectNameServiceTest, self).setUp()

        self.model_name = 'MyObjectName'
        self.service = MyObjectNameService()

        self.logger.debug('#### setUp END ####')

    def test_get_all(self):
        self.get_all()

    def test_get_by_pk(self):
        self.get_by_pk()
