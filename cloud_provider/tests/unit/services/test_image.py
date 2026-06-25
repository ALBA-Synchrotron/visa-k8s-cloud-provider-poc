# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from cloud_provider.services.image import ImageService
from cloud_provider.tests.utils.generic_service_test_case import MyGenericServiceTest


class ImageServiceTest(MyGenericServiceTest):
    fixtures: list = ["image.json"]

    def setUp(self) -> None:
        self.logger.debug("#### setUp START ####")
        super(ImageServiceTest, self).setUp()

        self.model_name: str = "Image"
        self.service = ImageService()

        self.logger.debug("#### setUp END ####")

    def test_get_all(self) -> None:
        self.get_all()

    def test_get_by_pk(self) -> None:
        self.get_by_pk()
