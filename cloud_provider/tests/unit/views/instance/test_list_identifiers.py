import logging

from rest_framework import status

from cloud_provider.labels.model import flavour as labels
from cloud_provider.models import Instance
from cloud_provider.services.instance import InstanceService
from mis_template.utils.test.generic_api_view_test_case import GenericApiViewTest


# forms test
class InstanceIDListViewTest(GenericApiViewTest):
    logger: logging.Logger = logging.getLogger(__name__)
    fixtures: list = ["image.json", "flavour.json", "security_group.json", "instance.json"]

    def setUp(self) -> None:
        super(InstanceIDListViewTest, self).setUp()
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

        self.logger.debug("#### setUp END ####")

    def test_get_instances_identifiers_list(self) -> None:
        self.login_and_check_http_methods(self.authorized_username, f"{self.url}/identifiers", ["GET", "POST"])

        response = self.client.get(f"{self.url}/identifiers")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        objects_in_db = self.model_class.objects.all().count()
        self.assertEqual(objects_in_db, len(response.json()))
