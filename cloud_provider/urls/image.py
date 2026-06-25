from django.urls import path

from cloud_provider.views.image import *

reference_name: str = "image"

urlpatterns: list = [
    path("api/images", ImagesList.as_view(), name=reference_name + "_list"),
    path("api/images/<int:image_id>", ImageDetail.as_view(), name=reference_name + "_detail"),
]
