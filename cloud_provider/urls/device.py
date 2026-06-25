from django.urls import path

from cloud_provider.views.device import *

reference_name: str = "device"

urlpatterns: list = [
    path("api/devices", DevicesList.as_view(), name=reference_name + "_list"),
    path("api/device/<str:device_type>/<str:device_identifier>", DeviceDetail.as_view(), name=reference_name + "_detail"),
    path("api/device_allocations", DeviceAllocations.as_view(), name=reference_name + "_allocations"),
]
