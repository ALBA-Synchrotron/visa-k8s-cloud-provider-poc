import logging

from cloud_provider.models import SecurityGroup
from cloud_provider.tests.utils.generic_model_test_case import MyGenericModelTestCase


class SecurityGroupModelTest(MyGenericModelTestCase):
    logger: logging.Logger = logging.getLogger(__name__)
    fixtures: list[str] = ["security_group.json"]

    def setUp(self) -> None:
        self.logger.debug("#### setUp START ####")
        super(SecurityGroupModelTest, self).setUp()

        self.model_class = SecurityGroup
        self.model_name: str = "security_group"
        self.mandatory_fields_json: dict = {
            "name": "SecurityGroup 1"
        }
        self.all_fields_json: dict = self.mandatory_fields_json  # All fields are mandatory

        self.existing_element_id: int = 1
        self.update_json: dict = {"name": "Updated security_group"}

        self.logger.debug("#### setUp END ####")

    def test_create(self) -> None:
        self.create()

    def test_update(self) -> None:
        self.update()
