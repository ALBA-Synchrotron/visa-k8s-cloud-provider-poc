import logging

from cloud_provider.models import ProposalAccount
from cloud_provider.tests.utils.generic_model_test_case import MyGenericModelTestCase
from mis_template.utils.models import TemplateModel


class ProposalAccountModelTest(MyGenericModelTestCase):
    logger: logging.Logger = logging.getLogger(__name__)
    fixtures: list[str] = ["proposal_account.json"]

    def setUp(self) -> None:
        self.logger.debug("#### setUp START ####")
        super(ProposalAccountModelTest, self).setUp()

        self.model_class: TemplateModel = ProposalAccount
        self.model_name: str = "proposal_account"
        self.mandatory_fields_json: dict = {
            "username": "PA 2",
            "uid": 8000002,
            "gid": 7000001,
        }
        self.all_fields_json: dict = {
            "username": "PA 3",
            "uid": 8000002,
            "gid": 7000001,
        }

        self.existing_element_id: int = 1
        self.update_json: dict = {"username": "Updated PA"}

        self.logger.debug("#### setUp END ####")

    def test_create(self) -> None:
        self.create()

    def test_update(self) -> None:
        self.update()
