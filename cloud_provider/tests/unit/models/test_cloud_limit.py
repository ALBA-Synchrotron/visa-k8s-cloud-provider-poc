import logging

from cloud_provider.models import CloudLimit
from cloud_provider.tests.utils.generic_model_test_case import MyGenericModelTestCase
from mis_template.utils.models import TemplateModel


class CloudLimitModelTest(MyGenericModelTestCase):
    logger: logging.Logger = logging.getLogger(__name__)
    fixtures: list[str] = ["cloud_limit.json"]

    def setUp(self) -> None:
        self.logger.debug("#### setUp START ####")
        super(CloudLimitModelTest, self).setUp()

        self.model_class: TemplateModel = CloudLimit
        self.model_name: str = "cloud_limit"
        self.mandatory_fields_json: dict = {
            "name": "LIMIT_1",
            "description": "Description 1",
            "value": 1000,
            "unit": "horses"
        }
        self.all_fields_json: dict = self.mandatory_fields_json  # All fields are mandatory

        self.existing_element_id: int = 1
        self.update_json: dict = {"name": "Updated flavour"}

        self.logger.debug("#### setUp END ####")

    def test_create(self) -> None:
        self.create()

    def test_update(self) -> None:
        self.update()
