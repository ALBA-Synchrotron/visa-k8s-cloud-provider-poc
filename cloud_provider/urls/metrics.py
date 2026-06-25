from django.urls import path

from cloud_provider.views.metrics import *

reference_name: str = "metrics"

urlpatterns: list = [
    path("api/metrics", MetricsView.as_view(), name=reference_name + "_detail"),
]
