# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.forms import ModelForm

from ..models.my_object_name import MyObjectName


class MyObjectNameForm(ModelForm):
    class Meta:
        model = MyObjectName
        fields = ['name']
