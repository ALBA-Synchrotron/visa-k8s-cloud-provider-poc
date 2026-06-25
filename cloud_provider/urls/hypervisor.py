from django.urls import path

from cloud_provider.views.hypervisor import *

reference_name: str = "hypervisor"

urlpatterns: list = [
    path("api/custom_resource_classes", CustomResourceClassesList.as_view(),
         name=reference_name + "_custom_resource_classes"),
    path("api/hypervisor_inventories", HypervisorInventoriesList.as_view(),
         name=reference_name + "_hypervisor_inventories"),
    path("api/hypervisor_usages", HypervisorUsagesList.as_view(),
         name=reference_name + "_hypervisor_usages"),
    path("api/hypervisor_allocations", HypervisorAllocationsList.as_view(),
         name=reference_name + "_hypervisor_allocations"),
]
