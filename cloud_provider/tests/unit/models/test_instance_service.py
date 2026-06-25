import logging

from cloud_provider.models import InstanceService
from cloud_provider.tests.utils.generic_model_test_case import MyGenericModelTestCase


class ProtocolModelTest(MyGenericModelTestCase):
    logger: logging.Logger = logging.getLogger(__name__)
    fixtures: list[str] = ["instance_service.json"]

    def setUp(self) -> None:
        self.logger.debug("#### setUp START ####")
        super(ProtocolModelTest, self).setUp()

        self.model_class = InstanceService
        self.model_name: str = "protocol"
        self.mandatory_fields_json: dict = {
            "name": "Protocol 1",
            "port": 2323,
            "protocol": "TCP",
            "bind_address": "0.0.0.0",
        }
        self.all_fields_json: dict = self.mandatory_fields_json  # All fields are mandatory

        self.existing_element_id: int = 1
        self.update_json: dict = {"name": "Updated protocol"}

        self.logger.debug("#### setUp END ####")

    def test_create(self) -> None:
        self.create()

    def test_update(self) -> None:
        self.update()
