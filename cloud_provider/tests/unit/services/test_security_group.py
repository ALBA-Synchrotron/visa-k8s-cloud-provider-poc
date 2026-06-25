# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from cloud_provider.services.security_group import SecurityGroupService
from cloud_provider.tests.utils.generic_service_test_case import MyGenericServiceTest


class SecurityGroupServiceTest(MyGenericServiceTest):
    fixtures: list = ["security_group.json"]

    def setUp(self) -> None:
        self.logger.debug("#### setUp START ####")
        super(SecurityGroupServiceTest, self).setUp()

        self.model_name: str = "SecurityGroup"
        self.service = SecurityGroupService()

        self.logger.debug("#### setUp END ####")

    def test_get_all(self) -> None:
        self.get_all()

    def test_get_by_pk(self) -> None:
        self.get_by_pk()
