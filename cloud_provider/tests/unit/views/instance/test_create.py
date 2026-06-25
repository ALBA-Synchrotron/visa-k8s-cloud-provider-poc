import json
import logging

from rest_framework import status

from cloud_provider.labels.model import flavour as labels
from cloud_provider.models import Instance
from cloud_provider.services.instance import InstanceService
from mis_template.utils.test.generic_api_view_test_case import GenericApiViewTest


# forms test
class InstanceCreateViewTest(GenericApiViewTest):
    logger: logging.Logger = logging.getLogger(__name__)
    fixtures: list = ["image.json", "flavour.json", "security_group.json", "instance.json", "cloud_limit.json"]

    def setUp(self) -> None:
        super(InstanceCreateViewTest, self).setUp()
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

    def test_create_instance(self) -> None:
        self.login(self.authorized_username)

        body: dict = {
            "name": "testing_asd",
            "imageId": "1",
            "flavourId": "1",
            "securityGroups": [],
            "metadata": {
                "owner": "rcabezas",
                "uid": "asldkas9823",
                "id": "29",
                "pamPublicKey": "lel"
            },
            "bootCommand": ""
        }

        response = self.client.post(f"{self.url}", data=json.dumps(body), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual("id" in response.data, True)

        invalid_body: dict = {
            "name": "testing_asd",
            "imageId": "13",
            "flavourId": "1",
            "securityGroups": [],
            "metadata": {
                "owner": "rcabezas",
                "uid": "asldkas9823",
                "id": "29",
                "pamPublicKey": "lel"
            },
            "bootCommand": ""
        }

        response = self.client.post(f"{self.url}", data=json.dumps(invalid_body), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        invalid_body: dict = {
            "name": "testing_asd",
            "imageId": "1",
            "flavourId": "123",
            "securityGroups": [],
            "metadata": {
                "owner": "rcabezas",
                "uid": "asldkas9823",
                "id": "29",
                "pamPublicKey": "lel"
            },
            "bootCommand": ""
        }

        response = self.client.post(f"{self.url}", data=json.dumps(invalid_body), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        invalid_body: dict = {
            "name": "testing_asd",
            "imageId": "1",
            "flavourId": "1",
            "securityGroups": ["LEL"],
            "metadata": {
                "owner": "rcabezas",
                "uid": "asldkas9823",
                "id": "29",
                "pamPublicKey": "lel"
            },
            "bootCommand": ""
        }

        response = self.client.post(f"{self.url}", data=json.dumps(invalid_body), content_type="application/json")
        self.assertEqual(response.status_code,
                         status.HTTP_201_CREATED)  # Non-existent groups are ignored on instance creation

        invalid_body: dict = {
            "name": "testing_asd",
            "imageId": "1",
            "flavourId": "1",
            "securityGroups": [],
            "metadata": {
                "owner": "rcabezas",
                "id": "29",
                "pamPublicKey": "lel"
            },
            "bootCommand": ""
        }

        response = self.client.post(f"{self.url}", data=json.dumps(invalid_body), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
