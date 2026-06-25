from django.urls import path, include
from cloud_provider.views.status import StatusView

urlpatterns: list = [
    path("", StatusView.as_view(), name="status"),
    path("<str:kubernetes_version>/", include("cloud_provider.urls.image")),
    path("<str:kubernetes_version>/", include("cloud_provider.urls.flavour")),
    path("<str:kubernetes_version>/", include("cloud_provider.urls.device")),
    path("<str:kubernetes_version>/", include("cloud_provider.urls.instance")),
    path("<str:kubernetes_version>/", include("cloud_provider.urls.metrics")),
    path("<str:kubernetes_version>/", include("cloud_provider.urls.security_group")),
    path("<str:kubernetes_version>/", include("cloud_provider.urls.hypervisor")),
    path("visa_sec_groups_svc/", include("cloud_provider.urls.instance_security_groups_svc")),
]
