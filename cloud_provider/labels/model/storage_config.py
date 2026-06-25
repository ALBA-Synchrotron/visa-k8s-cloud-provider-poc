# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ..generic.generic import *

MODEL_NAME: str = "storage_config"
MODEL_LABELS: dict = {
    "instrument": "Instrument",
    "read_only": "Read Only",
    "server": "Server",
    "server_path": "Server Path",
    "enabled": "Enabled",
    "home_directory_prefix": "Home Directory Prefix",
    "extra_nfs_gids": "Extra NFS GIDs",
    "scratch_server": "Scratch Server",
    "scratch_server_path": "Scratch Server Path",
    "scratch_enabled": "Scratch Enabled",
    "scratch_mount_path": "Scratch Mount Path",
    "scratch_read_only": "Scratch Read Only"
}
VERBOSE_NAME: str = "Storage Config"
