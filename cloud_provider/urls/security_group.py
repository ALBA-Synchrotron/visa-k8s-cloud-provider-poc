from django.urls import path

from cloud_provider.views.security_group import *

reference_name: str = "security_group"

urlpatterns: list = [
    path("api/security_groups", SecurityGroupList.as_view(), name=reference_name + "_list"),
]
