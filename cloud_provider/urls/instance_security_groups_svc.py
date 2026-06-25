from django.urls import path

from cloud_provider.views.instance_security_groups_svc import InstanceSecurityGroups

reference_name: str = "instance_security_group"

urlpatterns: list = [
    path("api/securitygroups/", InstanceSecurityGroups.as_view(), name=reference_name + "_detail"),
]
