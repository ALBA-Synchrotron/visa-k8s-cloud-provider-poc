import logging

from rest_framework import status

from cloud_provider.labels.model import flavour as labels
from cloud_provider.models import Instance
from cloud_provider.services.instance import InstanceService
from mis_template.utils.test.generic_api_view_test_case import GenericApiViewTest


# forms test
class InstanceCommandViewTest(GenericApiViewTest):
    logger: logging.Logger = logging.getLogger(__name__)
    fixtures: list = ["image.json", "flavour.json", "security_group.json", "instance.json"]

    def setUp(self) -> None:
        super(InstanceCommandViewTest, self).setUp()
        self.logger.debug("#### setUp START ####")

        self.model_name: str = "Instance"
        self.reference_name: str = "instance"
        self.service_class = InstanceService()
        self.model_class = Instance

        self.labels = labels

        self.is_cas_authenticated: bool = True
        self.check_unauthorized_user: bool = True
        self.check_authorized_user_list: list = [self.app_admin_username, self.app_manager_username]

        self.list_filter_list: list = [{}]

        self.url: str = "/v1.21.24/api/instances"
        self.existing_object: int = 1
        self.non_existent_id: int = 99999
        self.deleted_instance: int = 2

        self.logger.debug("#### setUp END ####")

    def test_start_instance(self) -> None:
        self.login(self.authorized_username)

        response = self.client.post(f"{self.url}/{self.existing_object}/start")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(f"{self.url}/{self.non_existent_id}/start")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.post(f"{self.url}/{self.deleted_instance}/start")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_shutdown_instance(self) -> None:
        self.login(self.authorized_username)

        response = self.client.post(f"{self.url}/{self.existing_object}/shutdown")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(f"{self.url}/{self.non_existent_id}/shutdown")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.post(f"{self.url}/{self.deleted_instance}/shutdown")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reboot_instance(self) -> None:
        self.login(self.authorized_username)

        response = self.client.post(f"{self.url}/{self.existing_object}/reboot")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(f"{self.url}/{self.non_existent_id}/reboot")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.post(f"{self.url}/{self.deleted_instance}/reboot")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_instance(self) -> None:
        self.login(self.authorized_username)

        response = self.client.delete(f"{self.url}/{self.existing_object}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.delete(f"{self.url}/{self.non_existent_id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.delete(f"{self.url}/{self.deleted_instance}")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)