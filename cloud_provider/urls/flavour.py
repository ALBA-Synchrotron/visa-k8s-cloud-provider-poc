from django.urls import path

from cloud_provider.views.flavour import *

reference_name: str = "flavour"

urlpatterns: list = [
    path("api/flavours", FlavoursList.as_view(), name=reference_name + "_list"),
    path("api/flavours/<int:flavour_id>", FlavourDetail.as_view(), name=reference_name + "_detail"),
    path("api/flavours/<int:flavour_id>/device_allocations", FlavourDeviceAllocations.as_view(), name=reference_name + "_device_allocations"),
]
