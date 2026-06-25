import logging

from rest_framework import status

from mis_template.utils.test.generic_api_view_test_case import GenericApiViewTest


# forms test


class DeviceAllocationsViewTest(GenericApiViewTest):
    logger: logging.Logger = logging.getLogger(__name__)
    fixtures: list = []

    def setUp(self) -> None:
        super(DeviceAllocationsViewTest, self).setUp()
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

        self.existing_object: int = 1
        self.not_existing_object: int = 9999
        self.url: str = "/v1.21.24/api/device_allocations"
        self.logger.debug("#### setUp END ####")

    def test_detail(self) -> None:
        self.login_and_check_http_methods(self.authorized_username, self.url.format(self.existing_object), ["GET"])

        # TODO: Endpoint needed as of VISA API server v3.6.0.
        #       This is a dummy implementation as we aren't integrating GPUs in our cloud provider.

        response = self.client.get(self.url.format(self.existing_object))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
