# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ..generic.generic import *

MODEL_NAME: str = "instance_service"
MODEL_LABELS: dict = {
    "name": "Name",
    "port": "Port",
    "bind_address": "Bind Address",
    "sidecar_deployed": "Sidecar Deployed",
    "container_image": "Container Image",
    "cpu_requests": "CPU Requests",
    "memory_requests": "Memory Requests",
    "cpu_limits": "CPU Limits",
    "memory_limits": "Memory Limits",
    "env_string": "Env String",
    "pull_secrets_name": "Pull Secrets Name",
    "pull_policy": "Pull Policy",
    "protocol": "Protocol",
    "mount_pvc_storage": "Mount PVC Storage",
    "command": "Command",
    "args": "Args",
    "mount_tmp_dir": "Mount /tmp dir",
    "mount_scratch_dir": "Mount Scratch Dir"
}
VERBOSE_NAME: str = "Instance Service"
