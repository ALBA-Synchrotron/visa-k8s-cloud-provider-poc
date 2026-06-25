import logging

from cloud_provider.models import Image
from cloud_provider.tests.utils.generic_model_test_case import MyGenericModelTestCase


class ImageModelTest(MyGenericModelTestCase):
    logger: logging.Logger = logging.getLogger(__name__)
    fixtures: list[str] = ["image.json"]

    def setUp(self) -> None:
        self.logger.debug("#### setUp START ####")
        super(ImageModelTest, self).setUp()

        self.model_class = Image
        self.model_name: str = "image"
        self.mandatory_fields_json: dict = {
            "name": "Image 1",
            "size": 12983.123,
            "full_image_url": "test.test/image-example:latest"
        }
        self.all_fields_json: dict = self.mandatory_fields_json  # All fields are mandatory

        self.existing_element_id: int = 1
        self.update_json: dict = {"name": "Updated image"}

        self.logger.debug("#### setUp END ####")

    def test_create(self) -> None:
        self.create()

    def test_update(self) -> None:
        self.update()
