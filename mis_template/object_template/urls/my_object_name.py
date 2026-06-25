from django.urls import path

from object_template.views.my_object_name import *

reference_name = 'my_object_name'

urlpatterns = [
    path('', List.as_view(), name=reference_name + '_list'),
    path('new/', Create.as_view(), name=reference_name + '_new'),
    path('<int:pk>/update/', Update.as_view(), name=reference_name + '_edit'),
    path('<int:pk>/delete/', Delete.as_view(), name=reference_name + '_delete'),
    path('<int:pk>', Detail.as_view(), name=reference_name + '_detail'),
]
