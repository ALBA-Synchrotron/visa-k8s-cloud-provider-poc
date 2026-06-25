# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from cloud_provider.services.instance import InstanceService
from cloud_provider.tests.utils.generic_service_test_case import MyGenericServiceTest


class InstanceServiceTest(MyGenericServiceTest):
    fixtures: list = ["flavour.json", "image.json", "security_group.json", "instance.json"]

    def setUp(self) -> None:
        self.logger.debug("#### setUp START ####")
        super(InstanceServiceTest, self).setUp()

        self.model_name: str = "Instance"
        self.service = InstanceService()

        self.logger.debug("#### setUp END ####")

    def test_get_all(self) -> None:
        self.get_all()

    def test_get_by_pk(self) -> None:
        self.get_by_pk()
