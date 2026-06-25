# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from cloud_provider.services.storage_config import StorageConfigService
from cloud_provider.tests.utils.generic_service_test_case import MyGenericServiceTest


class StorageConfigServiceTest(MyGenericServiceTest):
    fixtures: list = ["storage_config.json"]

    def setUp(self) -> None:
        self.logger.debug("#### setUp START ####")
        super(StorageConfigServiceTest, self).setUp()

        self.model_name = "StorageConfig"
        self.service = StorageConfigService()

        self.logger.debug("#### setUp END ####")

    def test_get_all(self) -> None:
        self.get_all()

    def test_get_by_pk(self) -> None:
        self.get_by_pk()
