import logging

from cloud_provider.models import HomeDirectory, ProposalAccount
from cloud_provider.tests.utils.generic_model_test_case import MyGenericModelTestCase
from mis_template.utils.models import TemplateModel


class HomeDirectoryModelTest(MyGenericModelTestCase):
    logger: logging.Logger = logging.getLogger(__name__)
    fixtures: list[str] = ["proposal_account.json", "home_directory.json"]

    def setUp(self) -> None:
        self.logger.debug("#### setUp START ####")
        super(HomeDirectoryModelTest, self).setUp()

        self.model_class: TemplateModel = HomeDirectory
        self.model_name: str = "proposal_account"

        self.mandatory_fields_json: dict = {
            "path": "/home/abc",
            "proposal_account": ProposalAccount.objects.get(pk=self.valid_id),
        }

        self.all_fields_json: dict = {
            "path": "/home/xyz",
            "proposal_account": ProposalAccount.objects.get(pk=self.valid_id),
        }

        self.existing_element_id: int = 1
        self.update_json: dict = {"path": "/home/updated"}

        self.logger.debug("#### setUp END ####")

    def test_create(self) -> None:
        self.create()

    def test_update(self) -> None:
        self.update()
