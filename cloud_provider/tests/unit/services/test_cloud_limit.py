# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from cloud_provider.services.cloud_limit import CloudLimitService
from cloud_provider.tests.utils.generic_service_test_case import MyGenericServiceTest


class CloudLimitServiceTest(MyGenericServiceTest):
    fixtures: list = ["cloud_limit.json"]

    def setUp(self) -> None:
        self.logger.debug("#### setUp START ####")
        super(CloudLimitServiceTest, self).setUp()

        self.model_name: str = "Flavour"
        self.service = CloudLimitService()

        self.logger.debug("#### setUp END ####")

    def test_get_all(self) -> None:
        self.get_all()

    def test_get_by_pk(self) -> None:
        self.get_by_pk()
