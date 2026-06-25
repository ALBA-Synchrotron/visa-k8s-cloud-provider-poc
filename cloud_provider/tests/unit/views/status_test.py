import logging

from django.urls import reverse
from rest_framework import status

from cloud_provider.tests.utils.generic_view_test_case import MyGenericViewTest


class StatusViewTest(MyGenericViewTest):
    logger: logging.Logger = logging.getLogger(__name__)

    def setUp(self) -> None:
        super(StatusViewTest, self).setUp()

    def test_status_endpoint(self) -> None:
        url = reverse("status")
        self.allowed_http_methods_testing(url, ["GET"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
