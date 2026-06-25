# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms

from object_template.labels.model import my_object_name as labels
from object_template.models import MyObjectName


class MyObjectNameFilterForm(forms.ModelForm):
    name = forms.CharField(required=False)

    class Meta:
        model = MyObjectName
        fields = ['name']
        labels = labels.FORM_LABELS
