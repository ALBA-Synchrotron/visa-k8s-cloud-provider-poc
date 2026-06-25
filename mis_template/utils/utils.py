# -*- coding: utf-8 -*-
from __future__ import unicode_literals


def beautify_string(string):
    string = string.replace("_", " ")
    return string.capitalize()


def round_of_rating(number):
    """
    :param number:
    :return: the number rounded to the closest integer or 0.5
    """
    return round(number * 2) / 2
