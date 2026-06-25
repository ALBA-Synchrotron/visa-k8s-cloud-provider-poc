from django.urls import path

from cloud_provider.views.instance import *

reference_name: str = "instance"

urlpatterns: list = [
    path("api/instances/<int:instance_id>/ip", InstanceAddressDetail.as_view(), name=reference_name + "_address"),
    path("api/instances", GeneralInstance.as_view(), name=reference_name + "_create_and_list"),
    path("api/instances/<int:instance_id>", DetailInstance.as_view(), name=reference_name + "_detail_and_delete"),
    path("api/instances/<int:instance_id>/start", StartInstance.as_view(), name=reference_name + "_start"),
    path("api/instances/<int:instance_id>/shutdown", ShutdownInstance.as_view(), name=reference_name + "_shutdown"),
    path("api/instances/<int:instance_id>/reboot", RebootInstance.as_view(), name=reference_name + "_reboot"),
    path("api/instances/identifiers", InstanceIdentifierList.as_view(), name=reference_name + "_identifiers"),
    path("api/instances/<int:instance_id>/security_groups", InstanceSecurityGroup.as_view(),
         name=reference_name + "_security_groups"),
    path("api/instances/<int:instance_id>/security_groups/remove", InstanceSecurityGroupRemove.as_view(),
         name=reference_name + "_security_groups_remove"),
]
