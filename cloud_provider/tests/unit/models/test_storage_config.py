import logging

from cloud_provider.models import StorageConfig
from cloud_provider.tests.utils.generic_model_test_case import MyGenericModelTestCase


class StorageConfigModelTest(MyGenericModelTestCase):
    logger: logging.Logger = logging.getLogger(__name__)
    fixtures: list[str] = ["storage_config.json"]

    def setUp(self) -> None:
        self.logger.debug("#### setUp START ####")
        super(StorageConfigModelTest, self).setUp()

        self.model_class = StorageConfig
        self.model_name: str = "storage_config"
        self.mandatory_fields_json: dict = {
            "instrument": "BL99 - Test",
            "read_only": True,
            "server": "test_server",
            "server_path": "/test/path",
            "enabled": True
        }
        self.all_fields_json: dict = self.mandatory_fields_json  # All fields are mandatory

        self.existing_element_id: int = 1
        self.update_json: dict = {"server": "updated_server"}

        self.logger.debug("#### setUp END ####")

    def test_create(self) -> None:
        self.create()

    def test_update(self) -> None:
        self.update()
