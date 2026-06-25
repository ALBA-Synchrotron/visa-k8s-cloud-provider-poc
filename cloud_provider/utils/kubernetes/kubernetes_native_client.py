from django.conf import settings
from kubernetes import config, client
from kubernetes.client import V1PodList, V1Deployment, V1DeploymentSpec, V1ObjectMeta, V1PodTemplateSpec, \
    V1LabelSelector, V1StatefulSet, V1StatefulSetSpec
from kubernetes.config import ConfigException


def get_apps_v1_api_client() -> client.AppsV1Api:
    if settings.TESTING_MODE:
        return AppsV1ApiMock()
    try:
        config.load_kube_config()
    except ConfigException:
        pass
    return client.AppsV1Api()


def get_core_v1_api_client() -> client.CoreV1Api:
    if settings.TESTING_MODE:
        return CoreV1ApiMock()
    try:
        config.load_kube_config()
    except ConfigException:
        pass
    return client.CoreV1Api()


class CoreV1ApiMock(client.CoreV1Api):

    def connect_delete_namespaced_pod_proxy(self, name, namespace, **kwargs):
        return None

    def connect_delete_namespaced_pod_proxy_with_http_info(self, name, namespace, **kwargs):
        return None

    def connect_delete_namespaced_pod_proxy_with_path(self, name, namespace, path, **kwargs):
        return None

    def connect_delete_namespaced_pod_proxy_with_path_with_http_info(self, name, namespace, path, **kwargs):
        return None

    def connect_delete_namespaced_service_proxy(self, name, namespace, **kwargs):
        return None

    def connect_delete_namespaced_service_proxy_with_http_info(self, name, namespace, **kwargs):
        return None

    def connect_delete_namespaced_service_proxy_with_path(self, name, namespace, path, **kwargs):
        return None

    def connect_delete_namespaced_service_proxy_with_path_with_http_info(self, name, namespace, path, **kwargs):
        return None

    def connect_delete_node_proxy(self, name, **kwargs):
        return None

    def connect_delete_node_proxy_with_http_info(self, name, **kwargs):
        return None

    def connect_delete_node_proxy_with_path(self, name, path, **kwargs):
        return None

    def connect_delete_node_proxy_with_path_with_http_info(self, name, path, **kwargs):
        return None

    def connect_get_namespaced_pod_attach(self, name, namespace, **kwargs):
        return None

    def connect_get_namespaced_pod_attach_with_http_info(self, name, namespace, **kwargs):
        return None

    def connect_get_namespaced_pod_exec(self, name, namespace, **kwargs):
        return None

    def connect_get_namespaced_pod_exec_with_http_info(self, name, namespace, **kwargs):
        return None

    def connect_get_namespaced_pod_portforward(self, name, namespace, **kwargs):
        return None

    def connect_get_namespaced_pod_portforward_with_http_info(self, name, namespace, **kwargs):
        return None

    def connect_get_namespaced_pod_proxy(self, name, namespace, **kwargs):
        return None

    def connect_get_namespaced_pod_proxy_with_http_info(self, name, namespace, **kwargs):
        return None

    def connect_get_namespaced_pod_proxy_with_path(self, name, namespace, path, **kwargs):
        return None

    def connect_get_namespaced_pod_proxy_with_path_with_http_info(self, name, namespace, path, **kwargs):
        return None

    def connect_get_namespaced_service_proxy(self, name, namespace, **kwargs):
        return None

    def connect_get_namespaced_service_proxy_with_http_info(self, name, namespace, **kwargs):
        return None

    def connect_get_namespaced_service_proxy_with_path(self, name, namespace, path, **kwargs):
        return None

    def connect_get_namespaced_service_proxy_with_path_with_http_info(self, name, namespace, path, **kwargs):
        return None

    def connect_get_node_proxy(self, name, **kwargs):
        return None

    def connect_get_node_proxy_with_http_info(self, name, **kwargs):
        return None

    def connect_get_node_proxy_with_path(self, name, path, **kwargs):
        return None

    def connect_get_node_proxy_with_path_with_http_info(self, name, path, **kwargs):
        return None

    def connect_head_namespaced_pod_proxy(self, name, namespace, **kwargs):
        return None

    def connect_head_namespaced_pod_proxy_with_http_info(self, name, namespace, **kwargs):
        return None

    def connect_head_namespaced_pod_proxy_with_path(self, name, namespace, path, **kwargs):
        return None

    def connect_head_namespaced_pod_proxy_with_path_with_http_info(self, name, namespace, path, **kwargs):
        return None

    def connect_head_namespaced_service_proxy(self, name, namespace, **kwargs):
        return None

    def connect_head_namespaced_service_proxy_with_http_info(self, name, namespace, **kwargs):
        return None

    def connect_head_namespaced_service_proxy_with_path(self, name, namespace, path, **kwargs):
        return None

    def connect_head_namespaced_service_proxy_with_path_with_http_info(self, name, namespace, path, **kwargs):
        return None

    def connect_head_node_proxy(self, name, **kwargs):
        return None

    def connect_head_node_proxy_with_http_info(self, name, **kwargs):
        return None

    def connect_head_node_proxy_with_path(self, name, path, **kwargs):
        return None

    def connect_head_node_proxy_with_path_with_http_info(self, name, path, **kwargs):
        return None

    def connect_options_namespaced_pod_proxy(self, name, namespace, **kwargs):
        return None

    def connect_options_namespaced_pod_proxy_with_http_info(self, name, namespace, **kwargs):
        return None

    def connect_options_namespaced_pod_proxy_with_path(self, name, namespace, path, **kwargs):
        return None

    def connect_options_namespaced_pod_proxy_with_path_with_http_info(self, name, namespace, path, **kwargs):
        return None

    def connect_options_namespaced_service_proxy(self, name, namespace, **kwargs):
        return None

    def connect_options_namespaced_service_proxy_with_http_info(self, name, namespace, **kwargs):
        return None

    def connect_options_namespaced_service_proxy_with_path(self, name, namespace, path, **kwargs):
        return None

    def connect_options_namespaced_service_proxy_with_path_with_http_info(self, name, namespace, path, **kwargs):
        return None

    def connect_options_node_proxy(self, name, **kwargs):
        return None

    def connect_options_node_proxy_with_http_info(self, name, **kwargs):
        return None

    def connect_options_node_proxy_with_path(self, name, path, **kwargs):
        return None

    def connect_options_node_proxy_with_path_with_http_info(self, name, path, **kwargs):
        return None

    def connect_patch_namespaced_pod_proxy(self, name, namespace, **kwargs):
        return None

    def connect_patch_namespaced_pod_proxy_with_http_info(self, name, namespace, **kwargs):
        return None

    def connect_patch_namespaced_pod_proxy_with_path(self, name, namespace, path, **kwargs):
        return None

    def connect_patch_namespaced_pod_proxy_with_path_with_http_info(self, name, namespace, path, **kwargs):
        return None

    def connect_patch_namespaced_service_proxy(self, name, namespace, **kwargs):
        return None

    def connect_patch_namespaced_service_proxy_with_http_info(self, name, namespace, **kwargs):
        return None

    def connect_patch_namespaced_service_proxy_with_path(self, name, namespace, path, **kwargs):
        return None

    def connect_patch_namespaced_service_proxy_with_path_with_http_info(self, name, namespace, path, **kwargs):
        return None

    def connect_patch_node_proxy(self, name, **kwargs):
        return None

    def connect_patch_node_proxy_with_http_info(self, name, **kwargs):
        return None

    def connect_patch_node_proxy_with_path(self, name, path, **kwargs):
        return None

    def connect_patch_node_proxy_with_path_with_http_info(self, name, path, **kwargs):
        return None

    def connect_post_namespaced_pod_attach(self, name, namespace, **kwargs):
        return None

    def connect_post_namespaced_pod_attach_with_http_info(self, name, namespace, **kwargs):
        return None

    def connect_post_namespaced_pod_exec(self, name, namespace, **kwargs):
        return None

    def connect_post_namespaced_pod_exec_with_http_info(self, name, namespace, **kwargs):
        return None

    def connect_post_namespaced_pod_portforward(self, name, namespace, **kwargs):
        return None

    def connect_post_namespaced_pod_portforward_with_http_info(self, name, namespace, **kwargs):
        return None

    def connect_post_namespaced_pod_proxy(self, name, namespace, **kwargs):
        return None

    def connect_post_namespaced_pod_proxy_with_http_info(self, name, namespace, **kwargs):
        return None

    def connect_post_namespaced_pod_proxy_with_path(self, name, namespace, path, **kwargs):
        return None

    def connect_post_namespaced_pod_proxy_with_path_with_http_info(self, name, namespace, path, **kwargs):
        return None

    def connect_post_namespaced_service_proxy(self, name, namespace, **kwargs):
        return None

    def connect_post_namespaced_service_proxy_with_http_info(self, name, namespace, **kwargs):
        return None

    def connect_post_namespaced_service_proxy_with_path(self, name, namespace, path, **kwargs):
        return None

    def connect_post_namespaced_service_proxy_with_path_with_http_info(self, name, namespace, path, **kwargs):
        return None

    def connect_post_node_proxy(self, name, **kwargs):
        return None

    def connect_post_node_proxy_with_http_info(self, name, **kwargs):
        return None

    def connect_post_node_proxy_with_path(self, name, path, **kwargs):
        return None

    def connect_post_node_proxy_with_path_with_http_info(self, name, path, **kwargs):
        return None

    def connect_put_namespaced_pod_proxy(self, name, namespace, **kwargs):
        return None

    def connect_put_namespaced_pod_proxy_with_http_info(self, name, namespace, **kwargs):
        return None

    def connect_put_namespaced_pod_proxy_with_path(self, name, namespace, path, **kwargs):
        return None

    def connect_put_namespaced_pod_proxy_with_path_with_http_info(self, name, namespace, path, **kwargs):
        return None

    def connect_put_namespaced_service_proxy(self, name, namespace, **kwargs):
        return None

    def connect_put_namespaced_service_proxy_with_http_info(self, name, namespace, **kwargs):
        return None

    def connect_put_namespaced_service_proxy_with_path(self, name, namespace, path, **kwargs):
        return None

    def connect_put_namespaced_service_proxy_with_path_with_http_info(self, name, namespace, path, **kwargs):
        return None

    def connect_put_node_proxy(self, name, **kwargs):
        return None

    def connect_put_node_proxy_with_http_info(self, name, **kwargs):
        return None

    def connect_put_node_proxy_with_path(self, name, path, **kwargs):
        return None

    def connect_put_node_proxy_with_path_with_http_info(self, name, path, **kwargs):
        return None

    def create_namespace(self, body, **kwargs):
        return None

    def create_namespace_with_http_info(self, body, **kwargs):
        return None

    def create_namespaced_binding(self, namespace, body, **kwargs):
        return None

    def create_namespaced_binding_with_http_info(self, namespace, body, **kwargs):
        return None

    def create_namespaced_config_map(self, namespace, body, **kwargs):
        return None

    def create_namespaced_config_map_with_http_info(self, namespace, body, **kwargs):
        return None

    def create_namespaced_endpoints(self, namespace, body, **kwargs):
        return None

    def create_namespaced_endpoints_with_http_info(self, namespace, body, **kwargs):
        return None

    def create_namespaced_event(self, namespace, body, **kwargs):
        return None

    def create_namespaced_event_with_http_info(self, namespace, body, **kwargs):
        return None

    def create_namespaced_limit_range(self, namespace, body, **kwargs):
        return None

    def create_namespaced_limit_range_with_http_info(self, namespace, body, **kwargs):
        return None

    def create_namespaced_persistent_volume_claim(self, namespace, body, **kwargs):
        return None

    def create_namespaced_persistent_volume_claim_with_http_info(self, namespace, body, **kwargs):
        return None

    def create_namespaced_pod(self, namespace, body, **kwargs):
        return None

    def create_namespaced_pod_with_http_info(self, namespace, body, **kwargs):
        return None

    def create_namespaced_pod_binding(self, name, namespace, body, **kwargs):
        return None

    def create_namespaced_pod_binding_with_http_info(self, name, namespace, body, **kwargs):
        return None

    def create_namespaced_pod_eviction(self, name, namespace, body, **kwargs):
        return None

    def create_namespaced_pod_eviction_with_http_info(self, name, namespace, body, **kwargs):
        return None

    def create_namespaced_pod_template(self, namespace, body, **kwargs):
        return None

    def create_namespaced_pod_template_with_http_info(self, namespace, body, **kwargs):
        return None

    def create_namespaced_replication_controller(self, namespace, body, **kwargs):
        return None

    def create_namespaced_replication_controller_with_http_info(self, namespace, body, **kwargs):
        return None

    def create_namespaced_resource_quota(self, namespace, body, **kwargs):
        return None

    def create_namespaced_resource_quota_with_http_info(self, namespace, body, **kwargs):
        return None

    def create_namespaced_secret(self, namespace, body, **kwargs):
        return None

    def create_namespaced_secret_with_http_info(self, namespace, body, **kwargs):
        return None

    def create_namespaced_service(self, namespace, body, **kwargs):
        return None

    def create_namespaced_service_with_http_info(self, namespace, body, **kwargs):
        return None

    def create_namespaced_service_account(self, namespace, body, **kwargs):
        return None

    def create_namespaced_service_account_with_http_info(self, namespace, body, **kwargs):
        return None

    def create_namespaced_service_account_token(self, name, namespace, body, **kwargs):
        return None

    def create_namespaced_service_account_token_with_http_info(self, name, namespace, body, **kwargs):
        return None

    def create_node(self, body, **kwargs):
        return None

    def create_node_with_http_info(self, body, **kwargs):
        return None

    def create_persistent_volume(self, body, **kwargs):
        return None

    def create_persistent_volume_with_http_info(self, body, **kwargs):
        return None

    def delete_collection_namespaced_config_map(self, namespace, **kwargs):
        return None

    def delete_collection_namespaced_config_map_with_http_info(self, namespace, **kwargs):
        return None

    def delete_collection_namespaced_endpoints(self, namespace, **kwargs):
        return None

    def delete_collection_namespaced_endpoints_with_http_info(self, namespace, **kwargs):
        return None

    def delete_collection_namespaced_event(self, namespace, **kwargs):
        return None

    def delete_collection_namespaced_event_with_http_info(self, namespace, **kwargs):
        return None

    def delete_collection_namespaced_limit_range(self, namespace, **kwargs):
        return None

    def delete_collection_namespaced_limit_range_with_http_info(self, namespace, **kwargs):
        return None

    def delete_collection_namespaced_persistent_volume_claim(self, namespace, **kwargs):
        return None

    def delete_collection_namespaced_persistent_volume_claim_with_http_info(self, namespace, **kwargs):
        return None

    def delete_collection_namespaced_pod(self, namespace, **kwargs):
        return None

    def delete_collection_namespaced_pod_with_http_info(self, namespace, **kwargs):
        return None

    def delete_collection_namespaced_pod_template(self, namespace, **kwargs):
        return None

    def delete_collection_namespaced_pod_template_with_http_info(self, namespace, **kwargs):
        return None

    def delete_collection_namespaced_replication_controller(self, namespace, **kwargs):
        return None

    def delete_collection_namespaced_replication_controller_with_http_info(self, namespace, **kwargs):
        return None

    def delete_collection_namespaced_resource_quota(self, namespace, **kwargs):
        return None

    def delete_collection_namespaced_resource_quota_with_http_info(self, namespace, **kwargs):
        return None

    def delete_collection_namespaced_secret(self, namespace, **kwargs):
        return None

    def delete_collection_namespaced_secret_with_http_info(self, namespace, **kwargs):
        return None

    def delete_collection_namespaced_service(self, namespace, **kwargs):
        return None

    def delete_collection_namespaced_service_with_http_info(self, namespace, **kwargs):
        return None

    def delete_collection_namespaced_service_account(self, namespace, **kwargs):
        return None

    def delete_collection_namespaced_service_account_with_http_info(self, namespace, **kwargs):
        return None

    def delete_collection_node(self, **kwargs):
        return None

    def delete_collection_node_with_http_info(self, **kwargs):
        return None

    def delete_collection_persistent_volume(self, **kwargs):
        return None

    def delete_collection_persistent_volume_with_http_info(self, **kwargs):
        return None

    def delete_namespace(self, name, **kwargs):
        return None

    def delete_namespace_with_http_info(self, name, **kwargs):
        return None

    def delete_namespaced_config_map(self, name, namespace, **kwargs):
        return None

    def delete_namespaced_config_map_with_http_info(self, name, namespace, **kwargs):
        return None

    def delete_namespaced_endpoints(self, name, namespace, **kwargs):
        return None

    def delete_namespaced_endpoints_with_http_info(self, name, namespace, **kwargs):
        return None

    def delete_namespaced_event(self, name, namespace, **kwargs):
        return None

    def delete_namespaced_event_with_http_info(self, name, namespace, **kwargs):
        return None

    def delete_namespaced_limit_range(self, name, namespace, **kwargs):
        return None

    def delete_namespaced_limit_range_with_http_info(self, name, namespace, **kwargs):
        return None

    def delete_namespaced_persistent_volume_claim(self, name, namespace, **kwargs):
        return None

    def delete_namespaced_persistent_volume_claim_with_http_info(self, name, namespace, **kwargs):
        return None

    def delete_namespaced_pod(self, name, namespace, **kwargs):
        return None

    def delete_namespaced_pod_with_http_info(self, name, namespace, **kwargs):
        return None

    def delete_namespaced_pod_template(self, name, namespace, **kwargs):
        return None

    def delete_namespaced_pod_template_with_http_info(self, name, namespace, **kwargs):
        return None

    def delete_namespaced_replication_controller(self, name, namespace, **kwargs):
        return None

    def delete_namespaced_replication_controller_with_http_info(self, name, namespace, **kwargs):
        return None

    def delete_namespaced_resource_quota(self, name, namespace, **kwargs):
        return None

    def delete_namespaced_resource_quota_with_http_info(self, name, namespace, **kwargs):
        return None

    def delete_namespaced_secret(self, name, namespace, **kwargs):
        return None

    def delete_namespaced_secret_with_http_info(self, name, namespace, **kwargs):
        return None

    def delete_namespaced_service(self, name, namespace, **kwargs):
        return None

    def delete_namespaced_service_with_http_info(self, name, namespace, **kwargs):
        return None

    def delete_namespaced_service_account(self, name, namespace, **kwargs):
        return None

    def delete_namespaced_service_account_with_http_info(self, name, namespace, **kwargs):
        return None

    def delete_node(self, name, **kwargs):
        return None

    def delete_node_with_http_info(self, name, **kwargs):
        return None

    def delete_persistent_volume(self, name, **kwargs):
        return None

    def delete_persistent_volume_with_http_info(self, name, **kwargs):
        return None

    def get_api_resources(self, **kwargs):
        return None

    def get_api_resources_with_http_info(self, **kwargs):
        return None

    def list_component_status(self, **kwargs):
        return None

    def list_component_status_with_http_info(self, **kwargs):
        return None

    def list_config_map_for_all_namespaces(self, **kwargs):
        return None

    def list_config_map_for_all_namespaces_with_http_info(self, **kwargs):
        return None

    def list_endpoints_for_all_namespaces(self, **kwargs):
        return None

    def list_endpoints_for_all_namespaces_with_http_info(self, **kwargs):
        return None

    def list_event_for_all_namespaces(self, **kwargs):
        return None

    def list_event_for_all_namespaces_with_http_info(self, **kwargs):
        return None

    def list_limit_range_for_all_namespaces(self, **kwargs):
        return None

    def list_limit_range_for_all_namespaces_with_http_info(self, **kwargs):
        return None

    def list_namespace(self, **kwargs):
        return None

    def list_namespace_with_http_info(self, **kwargs):
        return None

    def list_namespaced_config_map(self, namespace, **kwargs):
        return None

    def list_namespaced_config_map_with_http_info(self, namespace, **kwargs):
        return None

    def list_namespaced_endpoints(self, namespace, **kwargs):
        return None

    def list_namespaced_endpoints_with_http_info(self, namespace, **kwargs):
        return None

    def list_namespaced_event(self, namespace, **kwargs):
        return None

    def list_namespaced_event_with_http_info(self, namespace, **kwargs):
        return None

    def list_namespaced_limit_range(self, namespace, **kwargs):
        return None

    def list_namespaced_limit_range_with_http_info(self, namespace, **kwargs):
        return None

    def list_namespaced_persistent_volume_claim(self, namespace, **kwargs):
        return None

    def list_namespaced_persistent_volume_claim_with_http_info(self, namespace, **kwargs):
        return None

    def list_namespaced_pod(self, namespace, **kwargs):
        return V1PodList(items=[])

    def list_namespaced_pod_with_http_info(self, namespace, **kwargs):
        return None

    def list_namespaced_pod_template(self, namespace, **kwargs):
        return None

    def list_namespaced_pod_template_with_http_info(self, namespace, **kwargs):
        return None

    def list_namespaced_replication_controller(self, namespace, **kwargs):
        return None

    def list_namespaced_replication_controller_with_http_info(self, namespace, **kwargs):
        return None

    def list_namespaced_resource_quota(self, namespace, **kwargs):
        return None

    def list_namespaced_resource_quota_with_http_info(self, namespace, **kwargs):
        return None

    def list_namespaced_secret(self, namespace, **kwargs):
        return None

    def list_namespaced_secret_with_http_info(self, namespace, **kwargs):
        return None

    def list_namespaced_service(self, namespace, **kwargs):
        return None

    def list_namespaced_service_with_http_info(self, namespace, **kwargs):
        return None

    def list_namespaced_service_account(self, namespace, **kwargs):
        return None

    def list_namespaced_service_account_with_http_info(self, namespace, **kwargs):
        return None

    def list_node(self, **kwargs):
        return None

    def list_node_with_http_info(self, **kwargs):
        return None

    def list_persistent_volume(self, **kwargs):
        return None

    def list_persistent_volume_with_http_info(self, **kwargs):
        return None

    def list_persistent_volume_claim_for_all_namespaces(self, **kwargs):
        return None

    def list_persistent_volume_claim_for_all_namespaces_with_http_info(self, **kwargs):
        return None

    def list_pod_for_all_namespaces(self, **kwargs):
        return None

    def list_pod_for_all_namespaces_with_http_info(self, **kwargs):
        return None

    def list_pod_template_for_all_namespaces(self, **kwargs):
        return None

    def list_pod_template_for_all_namespaces_with_http_info(self, **kwargs):
        return None

    def list_replication_controller_for_all_namespaces(self, **kwargs):
        return None

    def list_replication_controller_for_all_namespaces_with_http_info(self, **kwargs):
        return None

    def list_resource_quota_for_all_namespaces(self, **kwargs):
        return None

    def list_resource_quota_for_all_namespaces_with_http_info(self, **kwargs):
        return None

    def list_secret_for_all_namespaces(self, **kwargs):
        return None

    def list_secret_for_all_namespaces_with_http_info(self, **kwargs):
        return None

    def list_service_account_for_all_namespaces(self, **kwargs):
        return None

    def list_service_account_for_all_namespaces_with_http_info(self, **kwargs):
        return None

    def list_service_for_all_namespaces(self, **kwargs):
        return None

    def list_service_for_all_namespaces_with_http_info(self, **kwargs):
        return None

    def patch_namespace(self, name, body, **kwargs):
        return None

    def patch_namespace_with_http_info(self, name, body, **kwargs):
        return None

    def patch_namespace_status(self, name, body, **kwargs):
        return None

    def patch_namespace_status_with_http_info(self, name, body, **kwargs):
        return None

    def patch_namespaced_config_map(self, name, namespace, body, **kwargs):
        return None

    def patch_namespaced_config_map_with_http_info(self, name, namespace, body, **kwargs):
        return None

    def patch_namespaced_endpoints(self, name, namespace, body, **kwargs):
        return None

    def patch_namespaced_endpoints_with_http_info(self, name, namespace, body, **kwargs):
        return None

    def patch_namespaced_event(self, name, namespace, body, **kwargs):
        return None

    def patch_namespaced_event_with_http_info(self, name, namespace, body, **kwargs):
        return None

    def patch_namespaced_limit_range(self, name, namespace, body, **kwargs):
        return None

    def patch_namespaced_limit_range_with_http_info(self, name, namespace, body, **kwargs):
        return None

    def patch_namespaced_persistent_volume_claim(self, name, namespace, body, **kwargs):
        return None

    def patch_namespaced_persistent_volume_claim_with_http_info(self, name, namespace, body, **kwargs):
        return None

    def patch_namespaced_persistent_volume_claim_status(self, name, namespace, body, **kwargs):
        return None

    def patch_namespaced_persistent_volume_claim_status_with_http_info(self, name, namespace, body, **kwargs):
        return None

    def patch_namespaced_pod(self, name, namespace, body, **kwargs):
        return None

    def patch_namespaced_pod_with_http_info(self, name, namespace, body, **kwargs):
        return None

    def patch_namespaced_pod_ephemeralcontainers(self, name, namespace, body, **kwargs):
        return None

    def patch_namespaced_pod_ephemeralcontainers_with_http_info(self, name, namespace, body, **kwargs):
        return None

    def patch_namespaced_pod_status(self, name, namespace, body, **kwargs):
        return None

    def patch_namespaced_pod_status_with_http_info(self, name, namespace, body, **kwargs):
        return None

    def patch_namespaced_pod_template(self, name, namespace, body, **kwargs):
        return None

    def patch_namespaced_pod_template_with_http_info(self, name, namespace, body, **kwargs):
        return None

    def patch_namespaced_replication_controller(self, name, namespace, body, **kwargs):
        return None

    def patch_namespaced_replication_controller_with_http_info(self, name, namespace, body, **kwargs):
        return None

    def patch_namespaced_replication_controller_scale(self, name, namespace, body, **kwargs):
        return None

    def patch_namespaced_replication_controller_scale_with_http_info(self, name, namespace, body, **kwargs):
        return None

    def patch_namespaced_replication_controller_status(self, name, namespace, body, **kwargs):
        return None

    def patch_namespaced_replication_controller_status_with_http_info(self, name, namespace, body, **kwargs):
        return None

    def patch_namespaced_resource_quota(self, name, namespace, body, **kwargs):
        return None

    def patch_namespaced_resource_quota_with_http_info(self, name, namespace, body, **kwargs):
        return None

    def patch_namespaced_resource_quota_status(self, name, namespace, body, **kwargs):
        return None

    def patch_namespaced_resource_quota_status_with_http_info(self, name, namespace, body, **kwargs):
        return None

    def patch_namespaced_secret(self, name, namespace, body, **kwargs):
        return None

    def patch_namespaced_secret_with_http_info(self, name, namespace, body, **kwargs):
        return None

    def patch_namespaced_service(self, name, namespace, body, **kwargs):
        return None

    def patch_namespaced_service_with_http_info(self, name, namespace, body, **kwargs):
        return None

    def patch_namespaced_service_account(self, name, namespace, body, **kwargs):
        return None

    def patch_namespaced_service_account_with_http_info(self, name, namespace, body, **kwargs):
        return None

    def patch_namespaced_service_status(self, name, namespace, body, **kwargs):
        return None

    def patch_namespaced_service_status_with_http_info(self, name, namespace, body, **kwargs):
        return None

    def patch_node(self, name, body, **kwargs):
        return None

    def patch_node_with_http_info(self, name, body, **kwargs):
        return None

    def patch_node_status(self, name, body, **kwargs):
        return None

    def patch_node_status_with_http_info(self, name, body, **kwargs):
        return None

    def patch_persistent_volume(self, name, body, **kwargs):
        return None

    def patch_persistent_volume_with_http_info(self, name, body, **kwargs):
        return None

    def patch_persistent_volume_status(self, name, body, **kwargs):
        return None

    def patch_persistent_volume_status_with_http_info(self, name, body, **kwargs):
        return None

    def read_component_status(self, name, **kwargs):
        return None

    def read_component_status_with_http_info(self, name, **kwargs):
        return None

    def read_namespace(self, name, **kwargs):
        return None

    def read_namespace_with_http_info(self, name, **kwargs):
        return None

    def read_namespace_status(self, name, **kwargs):
        return None

    def read_namespace_status_with_http_info(self, name, **kwargs):
        return None

    def read_namespaced_config_map(self, name, namespace, **kwargs):
        return None

    def read_namespaced_config_map_with_http_info(self, name, namespace, **kwargs):
        return None

    def read_namespaced_endpoints(self, name, namespace, **kwargs):
        return None

    def read_namespaced_endpoints_with_http_info(self, name, namespace, **kwargs):
        return None

    def read_namespaced_event(self, name, namespace, **kwargs):
        return None

    def read_namespaced_event_with_http_info(self, name, namespace, **kwargs):
        return None

    def read_namespaced_limit_range(self, name, namespace, **kwargs):
        return None

    def read_namespaced_limit_range_with_http_info(self, name, namespace, **kwargs):
        return None

    def read_namespaced_persistent_volume_claim(self, name, namespace, **kwargs):
        return None

    def read_namespaced_persistent_volume_claim_with_http_info(self, name, namespace, **kwargs):
        return None

    def read_namespaced_persistent_volume_claim_status(self, name, namespace, **kwargs):
        return None

    def read_namespaced_persistent_volume_claim_status_with_http_info(self, name, namespace, **kwargs):
        return None

    def read_namespaced_pod(self, name, namespace, **kwargs):
        return None

    def read_namespaced_pod_with_http_info(self, name, namespace, **kwargs):
        return None

    def read_namespaced_pod_ephemeralcontainers(self, name, namespace, **kwargs):
        return None

    def read_namespaced_pod_ephemeralcontainers_with_http_info(self, name, namespace, **kwargs):
        return None

    def read_namespaced_pod_log(self, name, namespace, **kwargs):
        return None

    def read_namespaced_pod_log_with_http_info(self, name, namespace, **kwargs):
        return None

    def read_namespaced_pod_status(self, name, namespace, **kwargs):
        return None

    def read_namespaced_pod_status_with_http_info(self, name, namespace, **kwargs):
        return None

    def read_namespaced_pod_template(self, name, namespace, **kwargs):
        return None

    def read_namespaced_pod_template_with_http_info(self, name, namespace, **kwargs):
        return None

    def read_namespaced_replication_controller(self, name, namespace, **kwargs):
        return None

    def read_namespaced_replication_controller_with_http_info(self, name, namespace, **kwargs):
        return None

    def read_namespaced_replication_controller_scale(self, name, namespace, **kwargs):
        return None

    def read_namespaced_replication_controller_scale_with_http_info(self, name, namespace, **kwargs):
        return None

    def read_namespaced_replication_controller_status(self, name, namespace, **kwargs):
        return None

    def read_namespaced_replication_controller_status_with_http_info(self, name, namespace, **kwargs):
        return None

    def read_namespaced_resource_quota(self, name, namespace, **kwargs):
        return None

    def read_namespaced_resource_quota_with_http_info(self, name, namespace, **kwargs):
        return None

    def read_namespaced_resource_quota_status(self, name, namespace, **kwargs):
        return None

    def read_namespaced_resource_quota_status_with_http_info(self, name, namespace, **kwargs):
        return None

    def read_namespaced_secret(self, name, namespace, **kwargs):
        return None

    def read_namespaced_secret_with_http_info(self, name, namespace, **kwargs):
        return None

    def read_namespaced_service(self, name, namespace, **kwargs):
        return None

    def read_namespaced_service_with_http_info(self, name, namespace, **kwargs):
        return None

    def read_namespaced_service_account(self, name, namespace, **kwargs):
        return None

    def read_namespaced_service_account_with_http_info(self, name, namespace, **kwargs):
        return None

    def read_namespaced_service_status(self, name, namespace, **kwargs):
        return None

    def read_namespaced_service_status_with_http_info(self, name, namespace, **kwargs):
        return None

    def read_node(self, name, **kwargs):
        return None

    def read_node_with_http_info(self, name, **kwargs):
        return None

    def read_node_status(self, name, **kwargs):
        return None

    def read_node_status_with_http_info(self, name, **kwargs):
        return None

    def read_persistent_volume(self, name, **kwargs):
        return None

    def read_persistent_volume_with_http_info(self, name, **kwargs):
        return None

    def read_persistent_volume_status(self, name, **kwargs):
        return None

    def read_persistent_volume_status_with_http_info(self, name, **kwargs):
        return None

    def replace_namespace(self, name, body, **kwargs):
        return None

    def replace_namespace_with_http_info(self, name, body, **kwargs):
        return None

    def replace_namespace_finalize(self, name, body, **kwargs):
        return None

    def replace_namespace_finalize_with_http_info(self, name, body, **kwargs):
        return None

    def replace_namespace_status(self, name, body, **kwargs):
        return None

    def replace_namespace_status_with_http_info(self, name, body, **kwargs):
        return None

    def replace_namespaced_config_map(self, name, namespace, body, **kwargs):
        return None

    def replace_namespaced_config_map_with_http_info(self, name, namespace, body, **kwargs):
        return None

    def replace_namespaced_endpoints(self, name, namespace, body, **kwargs):
        return None

    def replace_namespaced_endpoints_with_http_info(self, name, namespace, body, **kwargs):
        return None

    def replace_namespaced_event(self, name, namespace, body, **kwargs):
        return None

    def replace_namespaced_event_with_http_info(self, name, namespace, body, **kwargs):
        return None

    def replace_namespaced_limit_range(self, name, namespace, body, **kwargs):
        return None

    def replace_namespaced_limit_range_with_http_info(self, name, namespace, body, **kwargs):
        return None

    def replace_namespaced_persistent_volume_claim(self, name, namespace, body, **kwargs):
        return None

    def replace_namespaced_persistent_volume_claim_with_http_info(self, name, namespace, body, **kwargs):
        return None

    def replace_namespaced_persistent_volume_claim_status(self, name, namespace, body, **kwargs):
        return None

    def replace_namespaced_persistent_volume_claim_status_with_http_info(self, name, namespace, body, **kwargs):
        return None

    def replace_namespaced_pod(self, name, namespace, body, **kwargs):
        return None

    def replace_namespaced_pod_with_http_info(self, name, namespace, body, **kwargs):
        return None

    def replace_namespaced_pod_ephemeralcontainers(self, name, namespace, body, **kwargs):
        return None

    def replace_namespaced_pod_ephemeralcontainers_with_http_info(self, name, namespace, body, **kwargs):
        return None

    def replace_namespaced_pod_status(self, name, namespace, body, **kwargs):
        return None

    def replace_namespaced_pod_status_with_http_info(self, name, namespace, body, **kwargs):
        return None

    def replace_namespaced_pod_template(self, name, namespace, body, **kwargs):
        return None

    def replace_namespaced_pod_template_with_http_info(self, name, namespace, body, **kwargs):
        return None

    def replace_namespaced_replication_controller(self, name, namespace, body, **kwargs):
        return None

    def replace_namespaced_replication_controller_with_http_info(self, name, namespace, body, **kwargs):
        return None

    def replace_namespaced_replication_controller_scale(self, name, namespace, body, **kwargs):
        return None

    def replace_namespaced_replication_controller_scale_with_http_info(self, name, namespace, body, **kwargs):
        return None

    def replace_namespaced_replication_controller_status(self, name, namespace, body, **kwargs):
        return None

    def replace_namespaced_replication_controller_status_with_http_info(self, name, namespace, body, **kwargs):
        return None

    def replace_namespaced_resource_quota(self, name, namespace, body, **kwargs):
        return None

    def replace_namespaced_resource_quota_with_http_info(self, name, namespace, body, **kwargs):
        return None

    def replace_namespaced_resource_quota_status(self, name, namespace, body, **kwargs):
        return None

    def replace_namespaced_resource_quota_status_with_http_info(self, name, namespace, body, **kwargs):
        return None

    def replace_namespaced_secret(self, name, namespace, body, **kwargs):
        return None

    def replace_namespaced_secret_with_http_info(self, name, namespace, body, **kwargs):
        return None

    def replace_namespaced_service(self, name, namespace, body, **kwargs):
        return None

    def replace_namespaced_service_with_http_info(self, name, namespace, body, **kwargs):
        return None

    def replace_namespaced_service_account(self, name, namespace, body, **kwargs):
        return None

    def replace_namespaced_service_account_with_http_info(self, name, namespace, body, **kwargs):
        return None

    def replace_namespaced_service_status(self, name, namespace, body, **kwargs):
        return None

    def replace_namespaced_service_status_with_http_info(self, name, namespace, body, **kwargs):
        return None

    def replace_node(self, name, body, **kwargs):
        return None

    def replace_node_with_http_info(self, name, body, **kwargs):
        return None

    def replace_node_status(self, name, body, **kwargs):
        return None

    def replace_node_status_with_http_info(self, name, body, **kwargs):
        return None

    def replace_persistent_volume(self, name, body, **kwargs):
        return None

    def replace_persistent_volume_with_http_info(self, name, body, **kwargs):
        return None

    def replace_persistent_volume_status(self, name, body, **kwargs):
        return None

    def replace_persistent_volume_status_with_http_info(self, name, body, **kwargs):
        return None


class AppsV1ApiMock(client.AppsV1Api):
    """
    Mock implementation just to be used for the unit tests.
    Some dummy implementations may need to be reworked if something other than 'None' as return is expected.
    """

    def create_namespaced_controller_revision(self, namespace, body, **kwargs):
        return None

    def create_namespaced_controller_revision_with_http_info(self, namespace, body, **kwargs):
        return None

    def create_namespaced_daemon_set(self, namespace, body, **kwargs):
        return None

    def create_namespaced_daemon_set_with_http_info(self, namespace, body, **kwargs):
        return None

    def create_namespaced_deployment(self, namespace, body, **kwargs):
        return V1Deployment()

    def create_namespaced_deployment_with_http_info(self, namespace, body, **kwargs):
        return None

    def create_namespaced_replica_set(self, namespace, body, **kwargs):
        return None

    def create_namespaced_replica_set_with_http_info(self, namespace, body, **kwargs):
        return None

    def create_namespaced_stateful_set(self, namespace, body, **kwargs):
        return V1StatefulSet()

    def create_namespaced_stateful_set_with_http_info(self, namespace, body, **kwargs):
        return None

    def delete_collection_namespaced_controller_revision(self, namespace, **kwargs):
        return None

    def delete_collection_namespaced_controller_revision_with_http_info(self, namespace, **kwargs):
        return None

    def delete_collection_namespaced_daemon_set(self, namespace, **kwargs):
        return None

    def delete_collection_namespaced_daemon_set_with_http_info(self, namespace, **kwargs):
        return None

    def delete_collection_namespaced_deployment(self, namespace, **kwargs):
        return None

    def delete_collection_namespaced_deployment_with_http_info(self, namespace, **kwargs):
        return None

    def delete_collection_namespaced_replica_set(self, namespace, **kwargs):
        return None

    def delete_collection_namespaced_replica_set_with_http_info(self, namespace, **kwargs):
        return None

    def delete_collection_namespaced_stateful_set(self, namespace, **kwargs):
        return None

    def delete_collection_namespaced_stateful_set_with_http_info(self, namespace, **kwargs):
        return None

    def delete_namespaced_controller_revision(self, name, namespace, **kwargs):
        return None

    def delete_namespaced_controller_revision_with_http_info(self, name, namespace, **kwargs):
        return None

    def delete_namespaced_daemon_set(self, name, namespace, **kwargs):
        return None

    def delete_namespaced_daemon_set_with_http_info(self, name, namespace, **kwargs):
        return None

    def delete_namespaced_deployment(self, name, namespace, **kwargs):
        return V1Deployment()

    def delete_namespaced_deployment_with_http_info(self, name, namespace, **kwargs):
        return None

    def delete_namespaced_replica_set(self, name, namespace, **kwargs):
        return None

    def delete_namespaced_replica_set_with_http_info(self, name, namespace, **kwargs):
        return None

    def delete_namespaced_stateful_set(self, name, namespace, **kwargs):
        return V1StatefulSet()

    def delete_namespaced_stateful_set_with_http_info(self, name, namespace, **kwargs):
        return None

    def get_api_resources(self, **kwargs):
        return None

    def get_api_resources_with_http_info(self, **kwargs):
        return None

    def list_controller_revision_for_all_namespaces(self, **kwargs):
        return None

    def list_controller_revision_for_all_namespaces_with_http_info(self, **kwargs):
        return None

    def list_daemon_set_for_all_namespaces(self, **kwargs):
        return None

    def list_daemon_set_for_all_namespaces_with_http_info(self, **kwargs):
        return None

    def list_deployment_for_all_namespaces(self, **kwargs):
        return None

    def list_deployment_for_all_namespaces_with_http_info(self, **kwargs):
        return None

    def list_namespaced_controller_revision(self, namespace, **kwargs):
        return None

    def list_namespaced_controller_revision_with_http_info(self, namespace, **kwargs):
        return None

    def list_namespaced_daemon_set(self, namespace, **kwargs):
        return None

    def list_namespaced_daemon_set_with_http_info(self, namespace, **kwargs):
        return None

    def list_namespaced_deployment(self, namespace, **kwargs):
        return None

    def list_namespaced_deployment_with_http_info(self, namespace, **kwargs):
        return None

    def list_namespaced_replica_set(self, namespace, **kwargs):
        return None

    def list_namespaced_replica_set_with_http_info(self, namespace, **kwargs):
        return None

    def list_namespaced_stateful_set(self, namespace, **kwargs):
        return None

    def list_namespaced_stateful_set_with_http_info(self, namespace, **kwargs):
        return None

    def list_replica_set_for_all_namespaces(self, **kwargs):
        return None

    def list_replica_set_for_all_namespaces_with_http_info(self, **kwargs):
        return None

    def list_stateful_set_for_all_namespaces(self, **kwargs):
        return None

    def list_stateful_set_for_all_namespaces_with_http_info(self, **kwargs):
        return None

    def patch_namespaced_controller_revision(self, name, namespace, body, **kwargs):
        return None

    def patch_namespaced_controller_revision_with_http_info(self, name, namespace, body, **kwargs):
        return None

    def patch_namespaced_daemon_set(self, name, namespace, body, **kwargs):
        return None

    def patch_namespaced_daemon_set_with_http_info(self, name, namespace, body, **kwargs):
        return None

    def patch_namespaced_daemon_set_status(self, name, namespace, body, **kwargs):
        return None

    def patch_namespaced_daemon_set_status_with_http_info(self, name, namespace, body, **kwargs):
        return None

    def patch_namespaced_deployment(self, name, namespace, body, **kwargs):
        return V1Deployment()

    def patch_namespaced_deployment_with_http_info(self, name, namespace, body, **kwargs):
        return None

    def patch_namespaced_deployment_scale(self, name, namespace, body, **kwargs):
        return None

    def patch_namespaced_deployment_scale_with_http_info(self, name, namespace, body, **kwargs):
        return None

    def patch_namespaced_deployment_status(self, name, namespace, body, **kwargs):
        return None

    def patch_namespaced_deployment_status_with_http_info(self, name, namespace, body, **kwargs):
        return None

    def patch_namespaced_replica_set(self, name, namespace, body, **kwargs):
        return None

    def patch_namespaced_replica_set_with_http_info(self, name, namespace, body, **kwargs):
        return None

    def patch_namespaced_replica_set_scale(self, name, namespace, body, **kwargs):
        return None

    def patch_namespaced_replica_set_scale_with_http_info(self, name, namespace, body, **kwargs):
        return None

    def patch_namespaced_replica_set_status(self, name, namespace, body, **kwargs):
        return None

    def patch_namespaced_replica_set_status_with_http_info(self, name, namespace, body, **kwargs):
        return None

    def patch_namespaced_stateful_set(self, name, namespace, body, **kwargs):
        return V1StatefulSet()

    def patch_namespaced_stateful_set_with_http_info(self, name, namespace, body, **kwargs):
        return None

    def patch_namespaced_stateful_set_scale(self, name, namespace, body, **kwargs):
        return None

    def patch_namespaced_stateful_set_scale_with_http_info(self, name, namespace, body, **kwargs):
        return None

    def patch_namespaced_stateful_set_status(self, name, namespace, body, **kwargs):
        return None

    def patch_namespaced_stateful_set_status_with_http_info(self, name, namespace, body, **kwargs):
        return None

    def read_namespaced_controller_revision(self, name, namespace, **kwargs):
        return None

    def read_namespaced_controller_revision_with_http_info(self, name, namespace, **kwargs):
        return None

    def read_namespaced_daemon_set(self, name, namespace, **kwargs):
        return None

    def read_namespaced_daemon_set_with_http_info(self, name, namespace, **kwargs):
        return None

    def read_namespaced_daemon_set_status(self, name, namespace, **kwargs):
        return None

    def read_namespaced_daemon_set_status_with_http_info(self, name, namespace, **kwargs):
        return None

    def read_namespaced_deployment(self, name, namespace, **kwargs):
        v1_deployment = V1Deployment()
        v1_deployment.api_version = "apps/v1"
        v1_deployment.kind = "Deployment"

        selector_labels = {
            "environment": settings.DJANGO_ENV.lower(),
            "component": "visa-user-pod",
        }
        deployment_labels = {
            **selector_labels,
        }

        v1_deployment.metadata = V1ObjectMeta()

        v1_deployment.spec = V1DeploymentSpec(selector=V1LabelSelector(match_labels=selector_labels),
                                              template=V1PodTemplateSpec())
        v1_deployment.spec.replicas = 0
        v1_deployment.spec.template.metadata = V1ObjectMeta(labels=deployment_labels)

        return v1_deployment

    def read_namespaced_deployment_with_http_info(self, name, namespace, **kwargs):
        return None

    def read_namespaced_deployment_scale(self, name, namespace, **kwargs):
        return None

    def read_namespaced_deployment_scale_with_http_info(self, name, namespace, **kwargs):
        return None

    def read_namespaced_deployment_status(self, name, namespace, **kwargs):
        return None

    def read_namespaced_deployment_status_with_http_info(self, name, namespace, **kwargs):
        return None

    def read_namespaced_replica_set(self, name, namespace, **kwargs):
        return None

    def read_namespaced_replica_set_with_http_info(self, name, namespace, **kwargs):
        return None

    def read_namespaced_replica_set_scale(self, name, namespace, **kwargs):
        return None

    def read_namespaced_replica_set_scale_with_http_info(self, name, namespace, **kwargs):
        return None

    def read_namespaced_replica_set_status(self, name, namespace, **kwargs):
        return None

    def read_namespaced_replica_set_status_with_http_info(self, name, namespace, **kwargs):
        return None

    def read_namespaced_stateful_set(self, name, namespace, **kwargs):
        v1_statefulset = V1StatefulSet()
        v1_statefulset.api_version = "apps/v1"
        v1_statefulset.kind = "StatefulSet"

        selector_labels = {
            "environment": settings.DJANGO_ENV.lower(),
            "component": "visa-user-pod",
        }
        deployment_labels = {
            **selector_labels,
        }

        v1_statefulset.metadata = V1ObjectMeta()

        v1_statefulset.spec = V1StatefulSetSpec(selector=V1LabelSelector(match_labels=selector_labels),
                                                template=V1PodTemplateSpec(), replicas=0,
                                                service_name=f"{name}-svc")
        v1_statefulset.spec.replicas = 0
        v1_statefulset.spec.template.metadata = V1ObjectMeta(labels=deployment_labels)

        return v1_statefulset

    def read_namespaced_stateful_set_with_http_info(self, name, namespace, **kwargs):
        return None

    def read_namespaced_stateful_set_scale(self, name, namespace, **kwargs):
        return None

    def read_namespaced_stateful_set_scale_with_http_info(self, name, namespace, **kwargs):
        return None

    def read_namespaced_stateful_set_status(self, name, namespace, **kwargs):
        return None

    def read_namespaced_stateful_set_status_with_http_info(self, name, namespace, **kwargs):
        return None

    def replace_namespaced_controller_revision(self, name, namespace, body, **kwargs):
        return None

    def replace_namespaced_controller_revision_with_http_info(self, name, namespace, body, **kwargs):
        return None

    def replace_namespaced_daemon_set(self, name, namespace, body, **kwargs):
        return None

    def replace_namespaced_daemon_set_with_http_info(self, name, namespace, body, **kwargs):
        return None

    def replace_namespaced_daemon_set_status(self, name, namespace, body, **kwargs):
        return None

    def replace_namespaced_daemon_set_status_with_http_info(self, name, namespace, body, **kwargs):
        return None

    def replace_namespaced_deployment(self, name, namespace, body, **kwargs):
        return None

    def replace_namespaced_deployment_with_http_info(self, name, namespace, body, **kwargs):
        return None

    def replace_namespaced_deployment_scale(self, name, namespace, body, **kwargs):
        return None

    def replace_namespaced_deployment_scale_with_http_info(self, name, namespace, body, **kwargs):
        return None

    def replace_namespaced_deployment_status(self, name, namespace, body, **kwargs):
        return None

    def replace_namespaced_deployment_status_with_http_info(self, name, namespace, body, **kwargs):
        return None

    def replace_namespaced_replica_set(self, name, namespace, body, **kwargs):
        return None

    def replace_namespaced_replica_set_with_http_info(self, name, namespace, body, **kwargs):
        return None

    def replace_namespaced_replica_set_scale(self, name, namespace, body, **kwargs):
        return None

    def replace_namespaced_replica_set_scale_with_http_info(self, name, namespace, body, **kwargs):
        return None

    def replace_namespaced_replica_set_status(self, name, namespace, body, **kwargs):
        return None

    def replace_namespaced_replica_set_status_with_http_info(self, name, namespace, body, **kwargs):
        return None

    def replace_namespaced_stateful_set(self, name, namespace, body, **kwargs):
        return None

    def replace_namespaced_stateful_set_with_http_info(self, name, namespace, body, **kwargs):
        return None

    def replace_namespaced_stateful_set_scale(self, name, namespace, body, **kwargs):
        return None

    def replace_namespaced_stateful_set_scale_with_http_info(self, name, namespace, body, **kwargs):
        return None

    def replace_namespaced_stateful_set_status(self, name, namespace, body, **kwargs):
        return None

    def replace_namespaced_stateful_set_status_with_http_info(self, name, namespace, body, **kwargs):
        return None
