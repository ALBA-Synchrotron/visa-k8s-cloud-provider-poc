# -*- coding: utf-8 -*-
from __future__ import unicode_literals

APP_NAME: str = "alba-visa-k8s-cloud-provider"

# Generic formats
DATE_FORMAT: str = "%d-%m-%Y"
DATETIME_FORMAT: str = "%d-%m-%Y %H:%M"
DATE_FORMAT_EN: str = "%Y-%m-%d"
DATETIME_FORMAT_EN: str = "%Y-%m-%d %H:%M"
DATETIME_FORMAT_EN_SECONDS: str = "%Y-%m-%d %H:%M:%S"
# generic errors
ID_NOT_NULL: str = "id should not be null"
CONTROLLED_ERROR: str = "Controlled ERROR: %s"
PERMISSIONS_ERROR: str = "You do not have permissions to perform this action"
NOT_FOUND_ERROR: str = "The page you requested could not be found"

# To be overridden
MODEL_NAME: str = ""
LIST_HEADERS: list = []

DETAIL_TOOLTIP: str = "Detail"
EDIT_TOOLTIP: str = "Edit"
DELETE_TOOLTIP: str = "Delete"
PDF_TOOLTIP: str = "PDF"
RISK_ASSESSMENT_STATUS_HISTORY_TOOLTIP: str = "Status History"

INITIAL_VALUE_OPTION: str = "---------"
