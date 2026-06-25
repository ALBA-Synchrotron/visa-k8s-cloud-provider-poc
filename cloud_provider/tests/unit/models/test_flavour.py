import logging

from cloud_provider.models import Flavour
from cloud_provider.tests.utils.generic_model_test_case import MyGenericModelTestCase
from mis_template.utils.models import TemplateModel


class FlavourModelTest(MyGenericModelTestCase):
    logger: logging.Logger = logging.getLogger(__name__)
    fixtures: list[str] = ["flavour.json"]

    def setUp(self) -> None:
        self.logger.debug("#### setUp START ####")
        super(FlavourModelTest, self).setUp()

        self.model_class: TemplateModel = Flavour
        self.model_name: str = "flavour"
        self.mandatory_fields_json: dict = {
            "name": "Flavour 1",
            "cpus": 2,
            "ram": 1000,
            "disk": 50
        }
        self.all_fields_json: dict = self.mandatory_fields_json  # All fields are mandatory

        self.existing_element_id: int = 1
        self.update_json: dict = {"name": "Updated flavour"}

        self.logger.debug("#### setUp END ####")

    def test_create(self) -> None:
        self.create()

    def test_update(self) -> None:
        self.update()
