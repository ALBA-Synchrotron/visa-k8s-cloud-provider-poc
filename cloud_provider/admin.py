from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from cloud_provider.models import InstanceService, Flavour, Image, SecurityGroup, \
    Instance, ProposalAccount, StorageConfig, CloudLimit


@admin.register(InstanceService)
class InstanceServiceAdmin(SimpleHistoryAdmin):
    list_display = ("id", "name", "port", "bind_address", "sidecar_deployed")
    search_fields = ["id", "name", "port", "bind_address", "sidecar_deployed"]


@admin.register(Flavour)
class FlavourAdmin(SimpleHistoryAdmin):
    list_display = ("id", "name", "deleted")
    search_fields = ["id", "name", "deleted"]


@admin.register(Image)
class ImageAdmin(SimpleHistoryAdmin):
    list_display = ("id", "name", "size", "created_at", "full_image_url", "deleted")
    search_fields = ["id", "name", "size", "created_at", "full_image_url", "deleted"]


@admin.register(SecurityGroup)
class SecurityGroupAdmin(SimpleHistoryAdmin):
    list_display = ("id", "name")
    search_fields = ["id", "name"]


@admin.register(Instance)
class InstanceAdmin(SimpleHistoryAdmin):
    list_display = ("name", "flavour", "image", "active", "deployment_name")
    search_fields = ("name", "flavour", "image", "active", "deployment_name")


@admin.register(ProposalAccount)
class ProposalAccountAdmin(SimpleHistoryAdmin):
    list_display = ("username", "uid", "gid")
    search_fields = ("username", "uid", "gid")


@admin.register(StorageConfig)
class StorageConfigAdmin(SimpleHistoryAdmin):
    list_display = ("instrument", "read_only", "server", "server_path", "enabled", "scratch_enabled", "scratch_server")
    search_fields = ("instrument", "read_only", "server", "server_path", "enabled", "scratch_enabled", "scratch_server")


@admin.register(CloudLimit)
class CloudLimitAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "value")
    search_fields = ("name", "description")
