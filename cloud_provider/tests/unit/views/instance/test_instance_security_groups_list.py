import json
import logging

from rest_framework import status

from cloud_provider.labels.model import flavour as labels
from cloud_provider.models import Instance
from cloud_provider.services.instance import InstanceService
from mis_template.utils.test.generic_api_view_test_case import GenericApiViewTest


# forms test
class InstanceSecGroupListViewTest(GenericApiViewTest):
    logger: logging.Logger = logging.getLogger(__name__)
    fixtures: list = ["image.json", "flavour.json", "security_group.json", "instance.json"]

    def setUp(self) -> None:
        super(InstanceSecGroupListViewTest, self).setUp()
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

        self.url: str = "/v1.21.24/api/instances/{}/security_groups"
        self.existing_object: int = 1
        self.non_sec_group_object: int = 2
        self.non_existent_id: int = 99999

        self.logger.debug("#### setUp END ####")
        self.login(self.authorized_username)

    def test_get_instance_security_groups(self) -> None:
        response = self.client.get(self.url.format(self.existing_object))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(self.url.format(self.non_existent_id))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
