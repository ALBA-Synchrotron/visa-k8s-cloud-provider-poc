# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from cloud_provider.services.instance_service import InstanceServiceService
from cloud_provider.tests.utils.generic_service_test_case import MyGenericServiceTest


class ProtocolServiceTest(MyGenericServiceTest):
    fixtures: list = ["instance_service.json"]

    def setUp(self) -> None:
        self.logger.debug("#### setUp START ####")
        super(ProtocolServiceTest, self).setUp()

        self.model_name: str = "Protocol"
        self.service = InstanceServiceService()

        self.logger.debug("#### setUp END ####")

    def test_get_all(self) -> None:
        self.get_all()

    def test_get_by_pk(self) -> None:
        self.get_by_pk()
