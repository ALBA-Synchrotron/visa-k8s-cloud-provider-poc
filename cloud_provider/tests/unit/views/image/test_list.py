import logging

from rest_framework import status

from cloud_provider.labels.model import flavour as labels
from cloud_provider.services.flavour import FlavourService
from cloud_provider.tests.utils.generic_view_test_case import MyGenericViewTest
from mis_template.utils.test.generic_api_view_test_case import GenericApiViewTest


# forms test
class FlavourViewTest(GenericApiViewTest):
    logger: logging.Logger = logging.getLogger(__name__)
    fixtures: list = ["image.json"]

    def setUp(self) -> None:
        super(FlavourViewTest, self).setUp()
        self.logger.debug("#### setUp START ####")

        self.model_name: str = "Image"
        self.reference_name: str = "image"
        self.service_class = FlavourService()

        self.labels = labels

        self.is_cas_authenticated: bool = True
        self.check_unauthorized_user: bool = True
        self.check_authorized_user_list: list = [self.app_admin_username, self.app_manager_username]

        self.list_filter_list: list = [{}]

        self.url: str = "/v1.21.24/api/images"

        self.logger.debug("#### setUp END ####")

    def test_list(self) -> None:
        self.login_and_check_http_methods(self.authorized_username, self.url, ["GET"])

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
