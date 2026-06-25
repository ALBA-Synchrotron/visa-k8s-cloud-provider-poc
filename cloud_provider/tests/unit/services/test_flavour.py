# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from cloud_provider.services.flavour import FlavourService
from cloud_provider.tests.utils.generic_service_test_case import MyGenericServiceTest


class FlavourServiceTest(MyGenericServiceTest):
    fixtures: list = ["flavour.json"]

    def setUp(self) -> None:
        self.logger.debug("#### setUp START ####")
        super(FlavourServiceTest, self).setUp()

        self.model_name: str = "Flavour"
        self.service = FlavourService()

        self.logger.debug("#### setUp END ####")

    def test_get_all(self) -> None:
        self.get_all()

    def test_get_by_pk(self) -> None:
        self.get_by_pk()
