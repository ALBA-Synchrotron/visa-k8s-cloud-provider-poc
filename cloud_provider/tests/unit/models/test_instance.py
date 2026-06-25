import logging

from cloud_provider.models import Instance
from cloud_provider.tests.utils.generic_model_test_case import MyGenericModelTestCase


class InstanceModelTest(MyGenericModelTestCase):
    logger: logging.Logger = logging.getLogger(__name__)
    fixtures: list[str] = ["flavour.json", "image.json", "security_group.json", "instance.json"]

    def setUp(self) -> None:
        self.logger.debug("#### setUp START ####")
        super(InstanceModelTest, self).setUp()

        self.model_class = Instance
        self.model_name: str = "instance"
        self.mandatory_fields_json: dict = {
            "name": "Instance 1",
            "image_id": 1,
            "flavour_id": 1
        }
        self.all_fields_json: dict = self.mandatory_fields_json  # All fields are mandatory

        self.existing_element_id: int = 1
        self.update_json: dict = {"name": "Updated instance"}

        self.logger.debug("#### setUp END ####")

    def test_create(self) -> None:
        self.create()

    def test_update(self) -> None:
        self.update()
