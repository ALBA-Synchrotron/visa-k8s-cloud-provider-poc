# -*- coding: utf-8 -*-
from __future__ import unicode_literals


def get_filter_parameter(search_filter, parameter_name, return_list=False):
    if isinstance(search_filter.get(parameter_name), list):
        if len(search_filter.get(parameter_name)) > 1 or return_list:
            return search_filter.get(parameter_name)
        else:
            return search_filter.get(parameter_name)[0]
    else:
        return search_filter.get(parameter_name)


def request_filter_dict_to_initial_value_dict(filter_dict):
    initial_value = {}
    for key, value in filter_dict.items():
        initial_value[key] = get_filter_parameter(filter_dict, key)
    return initial_value
