import logging

from rest_framework import status

from mis_template.utils.test.generic_api_view_test_case import GenericApiViewTest


# forms test
class HypervisorAllocationsListViewTest(GenericApiViewTest):
    logger: logging.Logger = logging.getLogger(__name__)

    def setUp(self) -> None:
        super(HypervisorAllocationsListViewTest, self).setUp()
        self.logger.debug("#### setUp START ####")

        """
        self.model_name: str = "Flavour"
        self.reference_name: str = "flavour"
        self.service_class = FlavourService()

        self.labels = labels
        """

        self.is_cas_authenticated: bool = True
        self.check_unauthorized_user: bool = True
        self.check_authorized_user_list: list = [self.app_admin_username, self.app_manager_username]

        self.list_filter_list: list = [{}]

        self.url: str = "/v1.21.24/api/hypervisor_allocations"

        self.logger.debug("#### setUp END ####")

    def test_list(self) -> None:
        self.login_and_check_http_methods(self.authorized_username, self.url, ["GET"])

        # TODO: Endpoint needed as of VISA API server v3.6.0.
        #       This is a dummy implementation as we aren't integrating GPUs in our cloud provider.

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

