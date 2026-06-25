# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ..generic.generic import *

MODEL_NAME: str = "instance"
MODEL_LABELS: dict = {
    "name": "Name",
    "flavour": "Flavour",
    "image": "Image",
    "active": "Active",
    "created_at": "Created at",
    "updated_at": "Updated at",
    "deleted_at": "Deleted at",
    "visa_uid": "VISA UID",
    "address": "Address",
    "security_groups": "Security Groups",
    "deployment": "Deployment",
    "fault": "Fault",
    "deployment_name": "Deployment name",
    "deployment_representation": "Deployment representation",
    "associated_proposals": "Associated proposals",
}
VERBOSE_NAME: str = "Instance"
MSG_INSTANCE_DOES_NOT_EXIST: str = "Instance does not exist"
MSG_STARTING_INSTANCE: str = "Starting instance"
MSG_INSTANCE_DELETED: str = "Instance deleted, it cannot be started"
MSG_ERROR_STARTING_INSTANCE: str = "Error starting instance"
MSG_ERROR_STOPPING_INSTANCE: str = "Error stopping instance"
MSG_ERROR_CREATING_INSTANCE: str = "Error creating instance"
MSG_ERROR_REBOOTING_INSTANCE: str = "Error rebooting instance"
MSG_REBOOTING_INSTANCE: str = "Rebooting instance"
MSG_SHUTTING_DOWN_INSTANCE: str = "Shutting down instance"
MSG_DELETING_INSTANCE: str = "Deleting instance"
MSG_ERROR_DELETING_INSTANCE: str = "Error deleting instance"
MSG_ADDED_SECURITY_GROUP: str = "Added security group"
MSG_REMOVED_SECURITY_GROUP: str = "Removed security group"
MSG_SECURITY_GROUP_DOES_NOT_EXIST: str = "Security group does not exist"
MSG_SECURITY_GROUP_NOT_ASSIGNED_IN_INSTANCE: str = "Security group is not assigned in this instance"
