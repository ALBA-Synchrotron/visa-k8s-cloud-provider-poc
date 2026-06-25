import logging

from rest_framework import status

from cloud_provider.labels.model import flavour as labels
from cloud_provider.services.flavour import FlavourService
from cloud_provider.services.security_group import SecurityGroupService
from cloud_provider.tests.utils.generic_view_test_case import MyGenericViewTest
from mis_template.utils.test.generic_api_view_test_case import GenericApiViewTest


# forms test
class InstanceSecurityGroupSVCViewTest(GenericApiViewTest):
    logger: logging.Logger = logging.getLogger(__name__)
    fixtures: list = ["proposal_account.json", "home_directory.json"]

    def setUp(self) -> None:
        super(InstanceSecurityGroupSVCViewTest, self).setUp()
        self.logger.debug("#### setUp START ####")

        self.labels = labels

        self.is_cas_authenticated: bool = True
        self.check_unauthorized_user: bool = True
        self.check_authorized_user_list: list = [self.app_admin_username, self.app_manager_username]

        self.list_filter_list: list = [{}]

        self.url: str = "/visa_sec_groups_svc/api/securitygroups/"
        self.valid_body: dict = {
            "activeProtocols": [],
            "attributes": [],
            "cloudId": 3,
            "comments": None,
            "computeId": None,
            "createdAt": "2025-05-22T09:51:00.580+00:00",
            "deleteRequested": False,
            "deleted": False,
            "deletedAt": None,
            "experiments": [
                {
                    "doi": "",
                    "endDate": "2024-03-20T21:00:00.000+00:00",
                    "id": "2029097846",
                    "instrument": {
                        "id": 8,
                        "name": "BL16 - NOTOS"
                    },
                    "proposal": {
                        "doi": "",
                        "id": 2029097846,
                        "identifier": "2029097846",
                        "publicAt": "2027-03-21T05:00:00.000+00:00",
                        "summary": "TEST",
                        "title": "test",
                        "url": ""
                    },
                    "startDate": "2024-03-20T05:00:00.000+00:00",
                    "title": "test",
                    "url": ""
                },
                {
                    "doi": "",
                    "endDate": "2024-03-20T21:00:00.000+00:00",
                    "id": "2029097846",
                    "instrument": {
                        "id": 8,
                        "name": "BL16 - NOTOS"
                    },
                    "proposal": {
                        "doi": "",
                        "id": 2020097846,
                        "identifier": "2029097846",
                        "publicAt": "2027-03-21T05:00:00.000+00:00",
                        "summary": "TEST",
                        "title": "test",
                        "url": ""
                    },
                    "startDate": "2024-03-20T05:00:00.000+00:00",
                    "title": "test",
                    "url": ""
                }
            ],
            "expirationDate": None,
            "id": 245,
            "ipAddress": None,
            "keyboardLayout": "es-es-qwerty",
            "lastInteractionAt": "2025-05-22T09:51:00.580+00:00",
            "lastSeenAt": "2025-05-22T09:51:00.580+00:00",
            "members": [],
            "name": "tortoiseshell_baritone",
            "owner": {},
            "plan": {},
            "screenHeight": 1080,
            "screenWidth": 1920,
            "securityGroups": [],
            "state": "BUILDING",
            "stateHash": 1303535859,
            "terminationDate": "2025-07-21T09:51:00.580+00:00",
            "uid": "CRr7cxUv",
            "unrestrictedMemberAccess": None,
            "updatedAt": "2025-05-22T09:51:00.580+00:00",
            "username": "manoloooooo"
        }

        self.logger.debug("#### setUp END ####")

    def test_list(self) -> None:
        self.login_and_check_http_methods(self.authorized_username, self.url, ["POST"])

        response = self.client.post(self.url, data=self.valid_body, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("u2029097846", response.data)
        self.assertNotIn("u2020097846", response.data)
