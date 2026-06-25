import json
import re
from datetime import datetime

import pytz
from django.conf import settings
from kubernetes.client import V1Deployment, V1ObjectMeta, V1DeploymentSpec, V1LabelSelector, V1PodTemplateSpec, \
    V1Container, V1PodSpec, V1ContainerPort, V1ResourceRequirements, V1SecretReference, ApiException, V1EnvVar, \
    V1Volume, V1ConfigMapVolumeSource, V1KeyToPath, V1VolumeMount, V1StatefulSet, V1StatefulSetSpec, \
    V1LifecycleHandler, V1ExecAction, V1Lifecycle, V1NFSVolumeSource, V1PodSecurityContext, \
    V1PersistentVolumeClaimVolumeSource, V1PersistentVolumeClaim, V1PersistentVolumeClaimSpec, V1EmptyDirVolumeSource

from cloud_provider.models import Image, Flavour, Instance, SecurityGroup, ProposalAccount
from cloud_provider.services.storage_config import StorageConfigService
from cloud_provider.utils.dates import get_min_date
from cloud_provider.utils.kubernetes.kubernetes_native_client import get_apps_v1_api_client, \
    get_core_v1_api_client
from cloud_provider.utils.kubernetes.resource_metrics import get_total_commited_resources
from mis_template.models import Feature


class _KubernetesDeploymentClient:

    @classmethod
    def get_live_object(cls, instance: Instance = None, name: str = None):
        object_name = instance.deployment_name if instance else name
        if not object_name:
            return None

        client = get_apps_v1_api_client()
        try:
            live_object = client.read_namespaced_deployment(object_name,
                                                            settings.VISA_USER_POD_NAMESPACE)
        except ApiException as e:
            print(e)
            return None
        return live_object

    @classmethod
    def get_commited_resources(cls, namespace: str):
        client = get_apps_v1_api_client()
        try:
            deployments = client.list_namespaced_deployment(namespace).items
            total_cpu, total_mib = get_total_commited_resources(deployments)

        except ApiException as e:
            print(e)
            return -1
        return len(deployments), total_cpu, total_mib

    @classmethod
    def patch_live_object(cls, instance: Instance, live_object):
        client = get_apps_v1_api_client()
        try:
            live_object = client.patch_namespaced_deployment(instance.deployment_name,
                                                             settings.VISA_USER_POD_NAMESPACE, live_object)
        except ApiException as e:
            print(e)
            return None
        return live_object

    @classmethod
    def delete_live_object(cls, instance: Instance):
        client = get_apps_v1_api_client()
        try:
            live_object = client.delete_namespaced_deployment(instance.deployment_name,
                                                              settings.VISA_USER_POD_NAMESPACE)
        except ApiException as e:
            print(e)
            return None
        return live_object

    @classmethod
    def init_live_object(cls, visa_instance_name, metadata_labels, selector_labels):
        v1_deployment = V1Deployment()
        v1_deployment.api_version = "apps/v1"
        v1_deployment.kind = "Deployment"

        v1_deployment.metadata = V1ObjectMeta(labels=metadata_labels,
                                              name=visa_instance_name,
                                              namespace=settings.VISA_USER_POD_NAMESPACE)
        v1_deployment.spec = V1DeploymentSpec(selector=V1LabelSelector(match_labels=selector_labels),
                                              template=V1PodTemplateSpec(), replicas=0)
        v1_deployment.spec.template.metadata = V1ObjectMeta(labels=metadata_labels)

        return v1_deployment

    @classmethod
    def create_live_object(cls, live_object):
        client = get_apps_v1_api_client()
        try:
            live_object = client.create_namespaced_deployment(settings.VISA_USER_POD_NAMESPACE, live_object)
        except ApiException as e:
            print(e)
            return None
        return live_object


class _KubernetesStatefulSetClient:

    @classmethod
    def get_live_object(cls, instance: Instance = None, name: str = None):
        object_name = instance.deployment_name if instance else name
        if not object_name:
            return None

        client = get_apps_v1_api_client()
        try:
            live_object = client.read_namespaced_stateful_set(object_name,
                                                              settings.VISA_USER_POD_NAMESPACE)
        except ApiException as e:
            print(e)
            return None
        return live_object

    @classmethod
    def get_commited_resources(cls, namespace: str):
        client = get_apps_v1_api_client()
        try:
            statefulsets = client.list_namespaced_stateful_set(namespace).items
            total_cpu, total_mib = get_total_commited_resources(statefulsets)
        except ApiException as e:
            print(e)
            return -1
        return len(statefulsets), total_cpu, total_mib

    @classmethod
    def patch_live_object(cls, instance: Instance, live_object):
        client = get_apps_v1_api_client()
        try:
            live_object = client.patch_namespaced_stateful_set(instance.deployment_name,
                                                               settings.VISA_USER_POD_NAMESPACE, live_object)
        except ApiException as e:
            print(e)
            return None
        return live_object

    @classmethod
    def delete_live_object(cls, instance: Instance):
        client = get_apps_v1_api_client()
        client_core = get_core_v1_api_client()
        try:
            live_object = client.delete_namespaced_stateful_set(instance.deployment_name,
                                                                settings.VISA_USER_POD_NAMESPACE)
        except ApiException as e:
            print(e)
            return None
        return live_object

    @classmethod
    def init_live_object(cls, visa_instance_name, metadata_labels, selector_labels):
        v1_statefulset = V1StatefulSet()
        v1_statefulset.api_version = "apps/v1"
        v1_statefulset.kind = "StatefulSet"

        v1_statefulset.metadata = V1ObjectMeta(labels=metadata_labels,
                                               name=visa_instance_name,
                                               namespace=settings.VISA_USER_POD_NAMESPACE)
        v1_statefulset.spec = V1StatefulSetSpec(selector=V1LabelSelector(match_labels=selector_labels),
                                                template=V1PodTemplateSpec(), replicas=0,
                                                service_name=f"{visa_instance_name}-svc")
        v1_statefulset.spec.template.metadata = V1ObjectMeta(labels=metadata_labels)

        return v1_statefulset

    @classmethod
    def create_live_object(cls, live_object):
        client = get_apps_v1_api_client()
        try:
            live_object = client.create_namespaced_stateful_set(settings.VISA_USER_POD_NAMESPACE, live_object)
        except ApiException as e:
            print(e)
            return None
        return live_object


class KubernetesClient:

    @classmethod
    def get_commited_resources(cls):
        commited_instances, commited_cpu, commited_mib = cls.__get_backend_client().get_commited_resources(
            settings.VISA_USER_POD_NAMESPACE)
        return commited_instances, commited_cpu, commited_mib

    @classmethod
    def __get_backend_client(cls):
        if settings.VISA_CLOUD_PROVIDER_USE_STATEFULSET:
            return _KubernetesStatefulSetClient
        else:
            return _KubernetesDeploymentClient

    @classmethod
    def __clear_live_object_vcp_annotations(cls, live_object):
        if live_object.spec.template.metadata.annotations:
            for key in list(live_object.spec.template.metadata.annotations.keys()):
                if key.startswith("visa-cloud-provider/"):
                    del live_object.spec.template.metadata.annotations[key]
        return live_object

    @classmethod
    def __get_live_object_vcp_last_action(cls, live_object):
        if live_object.spec.template.metadata.annotations:
            for key in list(live_object.spec.template.metadata.annotations.keys()):
                if key.startswith("visa-cloud-provider/last_commanded_action"):
                    return live_object.spec.template.metadata.annotations[key]
        return None

    @classmethod
    def __set_live_object_status_vcp_annotations(cls, live_object, status: str):
        live_object.spec.template.metadata.annotations = {
            "visa-cloud-provider/last_action_datetime": datetime.now(tz=pytz.UTC)
            .isoformat(),
            "visa-cloud-provider/last_commanded_action": status
        }
        return live_object

    @classmethod
    def __get_live_pod_object(cls, name: str):
        client = get_core_v1_api_client()
        try:
            live_object = client.list_namespaced_pod(settings.VISA_USER_POD_NAMESPACE,
                                                     label_selector=f"name={name}")
        except ApiException as e:
            print(e)
            return None
        return live_object

    @classmethod
    def __kubernetize_string_for_name(cls, name: str):
        # Kubernetes ports cannot be named with more than 15 chars, no numbers or underscores and all in lowercase
        return re.sub('[^0-9a-zA-Z]+', '', name.lower().replace('_', '-'))[:14]

    @classmethod
    def __get_main_container_ports(cls, visa_instance: Instance):
        main_container_ports = [
            V1ContainerPort(container_port=service.port, name=cls.__kubernetize_string_for_name(service.name),
                            protocol=service.protocol, host_ip=service.bind_address, host_port=service.port) for
            service in
            visa_instance.flavour.instance_services.filter(sidecar_deployed=False).all()]
        return main_container_ports

    @classmethod
    def __get_additional_services_containers(cls, visa_instance: Instance, pvc_volume_mount=None,
                                             tmp_volume_mount=None, scratch_volume_mount=None):
        ret = []
        for additional_service in visa_instance.flavour.instance_services.filter(sidecar_deployed=True).all():
            port = V1ContainerPort(container_port=additional_service.port,
                                   name=cls.__kubernetize_string_for_name(additional_service.name),
                                   protocol=additional_service.protocol, host_ip=additional_service.bind_address,
                                   host_port=additional_service.port)
            container = V1Container(
                name=f"sidecar-svc-{cls.__kubernetize_string_for_name(additional_service.name)}",
                image=additional_service.container_image,
                image_pull_policy=additional_service.pull_policy if additional_service.pull_policy else 'IfNotPresent',
                ports=[port],
                env=[]
            )

            container_mounts = []
            if additional_service.mount_pvc_storage and pvc_volume_mount is not None:
                container_mounts.append(pvc_volume_mount)

            if additional_service.mount_tmp_dir and tmp_volume_mount is not None:
                container_mounts.append(tmp_volume_mount)

            if additional_service.mount_scratch_dir and scratch_volume_mount is not None:
                container_mounts.append(scratch_volume_mount)

            container.volume_mounts = container_mounts

            container_limits, container_requests = {}, {}
            if additional_service.cpu_requests:
                container_requests["cpu"] = additional_service.cpu_requests
            if additional_service.memory_requests:
                container_requests["memory"] = additional_service.memory_requests
            if additional_service.cpu_limits:
                container_limits["cpu"] = additional_service.cpu_limits
            if additional_service.memory_limits:
                container_limits["memory"] = additional_service.memory_limits

            container.resources = V1ResourceRequirements(limits=container_limits, requests=container_requests)

            if additional_service.env_string:
                env_var_list = additional_service.env_string.split("\n")
                for env_var in env_var_list:
                    env_var_key, env_var_value = env_var.split("=", maxsplit=1)
                    if env_var_key and env_var_value:
                        container.env.append(V1EnvVar(name=env_var_key.strip(), value=env_var_value.strip()))

            container.env.append(V1EnvVar(name="VISA_INSTANCE_ID", value=cls.__get_visa_instance_id(visa_instance)))
            container.env.append(V1EnvVar(name="VISA_PRINT_SERVER_AUTH_TOKEN", value=str(visa_instance.id)))
            container.env.append(V1EnvVar(name="NODE_FS_API_SERVER_AUTH_TOKEN", value=str(visa_instance.id)))
            container.env.append(V1EnvVar(name="VISA_INSTANCE_UID", value=str(visa_instance.visa_uid)))

            if additional_service.command:
                commands: list = additional_service.command.split(" ")
                container.command = [i.strip() for i in commands]

            if additional_service.args:
                if additional_service.args.startswith(">"):
                    container.args = [additional_service.args]
                else:
                    command_args: list = additional_service.args.split(" ")
                    container.args = [i.strip() for i in command_args]

            ret.append(container)
        return ret

    @classmethod
    def __get_visa_instance_id(cls, instance: Instance):
        return instance.name.replace(settings.VISA_INSTANCE_NAME_PREFIX, "")

    @classmethod
    def __get_visa_pam_public_key_mount(cls):
        # Define the volume from configmap
        visa_public_key_config_map_volume = V1Volume(
            name=settings.VISA_PUBLIC_KEY_NAME,
            config_map=V1ConfigMapVolumeSource(
                name=settings.VISA_PUBLIC_KEY_NAME,
                default_mode=0o644,
                items=[
                    V1KeyToPath(
                        key=settings.VISA_PUBLIC_KEY_FILENAME,
                        path=settings.VISA_PUBLIC_KEY_FILENAME
                    )
                ]
            )
        )

        visa_public_key_volume_mount = V1VolumeMount(
            name=settings.VISA_PUBLIC_KEY_NAME,
            mount_path=settings.VISA_PUBLIC_KEY_MOUNT_PATH,
            read_only=True
        )
        return visa_public_key_volume_mount, visa_public_key_config_map_volume

    @classmethod
    def __get_post_start_user_provision_command(cls, instance_name, users, image, sec_groups, gid=1001,
                                                base_uid=1999, supplemental_groups=None, su_usernames=None):
        supp_groups = []
        command = (
            f"ln -sf /usr/share/zoneinfo/{settings.VISA_INSTANCE_DEFAULT_TIMEZONE} /etc/localtime && echo {settings.VISA_INSTANCE_DEFAULT_TIMEZONE} > /etc/timezone "
            f" && groupadd -g {gid} {instance_name}")

        for i, user in enumerate(users):
            command += (
                f" && mkdir -p /home/{user} && useradd -u {base_uid + i} -g {instance_name} {f"-s {image.user_shell}" if image.user_shell else ""}"
                f" -d /home/{user} {f'-G {",".join(supplemental_groups)}' if supplemental_groups else ''} {user} "
                f"{f"&& cp -rf {image.home_template_path}. /home/{user}/" if image.home_template_path else ""}"
                f" && echo 'export TZ={settings.VISA_INSTANCE_DEFAULT_TIMEZONE}' >> /home/{user}/.bashrc && chown -Rf {user}:{instance_name} /home/{user}")
            if settings.VISA_INSTANCE_SUDOERS_SECURITY_GROUPS in sec_groups:
                command += f" && echo '{user} ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers"
            if su_usernames:
                sudo_su_prop_feature = Feature.objects.get(code="ENABLE_SUDO_SU_PROP_ACCOUNT")
                if sudo_su_prop_feature and sudo_su_prop_feature.enabled:
                    for j in su_usernames:
                        command += f" && echo '{user} ALL=(ALL) NOPASSWD: /bin/su {j}' >> /etc/sudoers"

        return command

    @classmethod
    def __get_post_start_data_access_symbolic_link_command(cls, investigation_paths):
        command = f"mkdir -p /investigation-data"

        for i in investigation_paths:
            inv_dir = i.split("/")[-1]
            command += f" && ln -s {i} /investigation-data/{inv_dir}"

        return command

    @classmethod
    def __get_supplemental_groups_provision_command(cls, supplemental_groups) -> (str, list):
        commands: list = []
        supp_groups: list = []
        for i, group in enumerate(supplemental_groups):
            commands.append(f"groupadd -g {group} group{i + 1}")
            supp_groups.append(f"group{i + 1}")
        return " && ".join(commands), supp_groups

    @classmethod
    def __get_post_start_proposal_account_provision_command(cls, associated_proposals, image,
                                                            supplemental_groups=None) -> (str, list):
        usernames: list = []
        commands: list = []
        for i in associated_proposals:
            home_dir = i.home_directory_list.last()
            commands.append(f"useradd -u {i.uid} -g {i.gid} {f"-s {image.user_shell}" if image.user_shell else ""}"
                            f" {f"-d {home_dir.path}" if home_dir else ""} {f'-G {",".join(supplemental_groups)}' if supplemental_groups else ''}"
                            f" {i.username}")
            usernames.append(i.username)
        return " && ".join(commands), usernames

    @classmethod
    def __get_container_post_start_lifecycle(cls, instance, users, image, sec_groups, supplemental_groups=None,
                                             investigation_paths=None):
        command, supp_groups = "", None

        command += f"mkdir -p /var/visa/ && echo {instance.id} > /var/visa/instance_id && chmod 444 /var/visa/instance_id"

        if supplemental_groups:
            groups_command, supp_groups = cls.__get_supplemental_groups_provision_command(supplemental_groups)
            command += f" && {groups_command}"

        command_proposal_accounts, proposal_usernames = cls.__get_post_start_proposal_account_provision_command(
            instance.associated_proposals.all(), image, supplemental_groups=supp_groups)
        if command_proposal_accounts:
            command += f" && {command_proposal_accounts}"

        if command:
            command += " && "
        command += f"{cls.__get_post_start_user_provision_command(instance.deployment_name, users, image, sec_groups,
                                                                  supplemental_groups=supp_groups, su_usernames=proposal_usernames)}"

        if investigation_paths:
            command += f" && {cls.__get_post_start_data_access_symbolic_link_command(investigation_paths)}"

        exec_action = V1ExecAction(command=["/bin/sh", "-c", command])
        life_cycle_handler = V1LifecycleHandler(_exec=exec_action)
        life_cycle = V1Lifecycle(post_start=life_cycle_handler)
        return life_cycle

    @classmethod
    def __fetch_storage_config_for_instance(cls, instance: Instance):
        storage_config_list = {}
        for storage_config in StorageConfigService().get_all():
            for proposal in instance.associated_proposals.all():
                for home_directory in proposal.home_directory_list.all():
                    if home_directory.path.startswith(storage_config.home_directory_prefix):
                        if storage_config.instrument not in storage_config_list:
                            storage_config_list[storage_config.instrument] = {"config": storage_config,
                                                                              "proposals": [proposal]}
                            break
                        else:
                            storage_config_list[storage_config.instrument]["proposals"].append(proposal)
                            break
                if proposal in storage_config_list.get(storage_config.instrument, {}).get("proposals", []):
                    break

        return storage_config_list

    @classmethod
    def __get_instrument_storage_volumes_mounts_and_gid_values(cls, instance: Instance):
        volumes, volume_mounts, gids, investigation_paths = [], [], [], []
        storage_configs = cls.__fetch_storage_config_for_instance(instance)
        scratch_volume_mount = None

        for instrument in storage_configs:
            nfs_volume_source = V1NFSVolumeSource(
                server=storage_configs[instrument]["config"].server,
                path=storage_configs[instrument]["config"].server_path,
                read_only=storage_configs[instrument]["config"].read_only
            )
            volume_name = f"nfs-{cls.__kubernetize_string_for_name(instrument)}-storage"
            volume = V1Volume(nfs=nfs_volume_source, name=volume_name)
            volumes.append(volume)

            if storage_configs[instrument]["config"].extra_nfs_gids:
                nfs_gids = [int(i) for i in storage_configs[instrument]["config"].extra_nfs_gids.split(",") if i]
                gids.extend(nfs_gids)

            for proposal in storage_configs[instrument]["proposals"]:
                home_dir_amount = len(proposal.home_directory_list.all())

                gids.append(int(proposal.gid))
                investigation_paths.extend([i.path for i in proposal.home_directory_list.all()])

                for i, home_directory in enumerate(proposal.home_directory_list.all()):
                    """
                    # subpath does not work for us due to the way the NFS exports are configured.
                    sub_path = home_directory.path.removeprefix(storage_configs[instrument]["config"].home_directory_prefix)
                    volume_mount_name = f"proposal-{proposal.username}-{i}".replace("u", "")
                    if sub_path.startswith("/"):
                        sub_path = sub_path[1:]
                    mount_path = f"{settings.VISA_STORAGE_MOUNT_PREFIX}/{volume_mount_name}" if home_dir_amount == 1 \
                        else f"{settings.VISA_STORAGE_MOUNT_PREFIX}/{home_directory.path}-{i + 1}"
                    """

                    volume_mount = V1VolumeMount(name=volume_name,
                                                 read_only=storage_configs[instrument]["config"].read_only,
                                                 mount_path=storage_configs[instrument]["config"].home_directory_prefix,
                                                 )
                    volume_mounts.append(volume_mount)

            if storage_configs[instrument]["config"].scratch_enabled:
                if not scratch_volume_mount:
                    scratch_volume_source = V1NFSVolumeSource(
                        server=storage_configs[instrument]["config"].scratch_server,
                        path=storage_configs[instrument]["config"].scratch_server_path,
                        read_only=storage_configs[instrument]["config"].scratch_read_only
                    )
                    scratch_volume_name = f"nfs-{cls.__kubernetize_string_for_name(instrument)}-hpc-scratch"
                    scratch_volume = V1Volume(nfs=scratch_volume_source, name=scratch_volume_name)
                    volumes.append(scratch_volume)

                    scratch_volume_mount = V1VolumeMount(name=scratch_volume_name,
                                                         read_only=storage_configs[instrument]["config"].scratch_read_only,
                                                         mount_path=storage_configs[instrument][
                                                             "config"].scratch_mount_path,
                                                         )
                    volume_mounts.append(scratch_volume_mount)

        return volumes, volume_mounts, list(set(gids)), investigation_paths, scratch_volume_mount

    @classmethod
    def __delete_instance_pvc(cls, instance):
        client = get_core_v1_api_client()
        pvc = None
        try:
            pvc = client.read_namespaced_persistent_volume_claim(f"{instance.deployment_name}-pvc",
                                                                 settings.VISA_USER_POD_NAMESPACE)
        except ApiException as e:
            print(e)
            return
        if pvc:
            try:
                _ = client.delete_namespaced_persistent_volume_claim(f"{instance.deployment_name}-pvc",
                                                                     settings.VISA_USER_POD_NAMESPACE)
            except ApiException as e:
                print(e)
                return

    @classmethod
    def __provision_pvc_retrieve_volume_and_mounts(cls, instance):
        if not instance.flavour.mount_pvc_storage:
            return None, None
        pvc = V1PersistentVolumeClaim(
            metadata=V1ObjectMeta(name=f"{instance.deployment_name}-pvc"),
            spec=V1PersistentVolumeClaimSpec(
                access_modes=[settings.VISA_INSTANCE_PERSISTENCE_ACCESS_MODE],
                resources=V1ResourceRequirements(
                    requests={"storage": f"{instance.flavour.disk}Mi"}
                ),
                storage_class_name=settings.VISA_INSTANCE_PERSISTENCE_STORAGE_CLASS
            )
        )

        client = get_core_v1_api_client()
        try:
            _ = client.create_namespaced_persistent_volume_claim(
                settings.VISA_USER_POD_NAMESPACE, pvc)
        except ApiException as e:
            print(e)
            return None, None
        pvc_volume = V1Volume(
            name=f"{instance.deployment_name}-pvc-volume",
            persistent_volume_claim=V1PersistentVolumeClaimVolumeSource(
                claim_name=pvc.metadata.name,
                read_only=False
            )
        )
        pvc_volume_mount = V1VolumeMount(
            name=f"{instance.deployment_name}-pvc-volume",
            mount_path=settings.VISA_INSTANCE_PERSISTENCE_MOUNT_PATH,
            read_only=False
        )
        return pvc_volume, pvc_volume_mount

    @classmethod
    def start_visa_instance(cls, instance: Instance) -> Instance or None:
        live_object = cls.__get_backend_client().get_live_object(instance=instance)

        if not live_object:
            return None

        live_object.spec.replicas = 1
        live_object = cls.__clear_live_object_vcp_annotations(live_object)
        live_object = cls.__set_live_object_status_vcp_annotations(live_object, "start")
        live_object = cls.__get_backend_client().patch_live_object(instance, live_object)

        if live_object:
            instance.active = True
            instance.deployment_representation = json.dumps(live_object.to_dict(), default=str)
            instance.save()
            return instance
        return None

    @classmethod
    def delete_visa_instance(cls, instance: Instance) -> Instance or None:
        live_object = cls.__get_backend_client().delete_live_object(instance)

        if live_object:
            if instance.flavour.mount_pvc_storage:
                cls.__delete_instance_pvc(instance)

            instance.active = False
            instance.deleted_at = datetime.now(pytz.UTC)
            instance.deployment_representation = json.dumps(live_object.to_dict(), default=str)
            instance.save()
            return instance
        return None

    @classmethod
    def stop_visa_instance(cls, instance: Instance) -> Instance or None:
        live_object = cls.__get_backend_client().get_live_object(instance=instance)
        if not live_object:
            return None

        live_object.spec.replicas = 0
        live_object = cls.__clear_live_object_vcp_annotations(live_object)
        live_object = cls.__set_live_object_status_vcp_annotations(live_object, "stop")
        live_object = cls.__get_backend_client().patch_live_object(instance, live_object)

        if live_object:
            instance.active = False
            instance.deployment_representation = json.dumps(live_object.to_dict(), default=str)
            instance.save()
            return instance
        return None

    @classmethod
    def reboot_visa_instance(cls, instance: Instance) -> Instance or None:
        live_object = cls.__get_backend_client().get_live_object(instance=instance)
        if not live_object:
            return None

        live_object = cls.__clear_live_object_vcp_annotations(live_object)
        live_object = cls.__set_live_object_status_vcp_annotations(live_object, "reboot")
        live_object = cls.__get_backend_client().patch_live_object(instance, live_object)

        if live_object:
            instance.deployment_representation = json.dumps(live_object.to_dict(), default=str)
            instance.save()
            return instance
        return None

    @classmethod
    def visa_instance_has_fault(cls, name: str) -> bool:
        live_object_pod = cls.__get_live_pod_object(name)

        if not live_object_pod.items:
            return False

        pod = live_object_pod.items[0]
        for container_status in pod.status.container_statuses:
            state = container_status.state
            if state.waiting:
                reason = state.waiting.reason or ""
                if reason not in ["ContainerCreating", "PodInitializing", "Terminating"]:
                    return True

            if state.terminated:
                return True
        return False

    @classmethod
    def get_visa_instance_ip(cls, name: str) -> str or None:
        live_object_pod = cls.__get_live_pod_object(name)
        if live_object_pod and live_object_pod.items:
            return live_object_pod.items[0].status.pod_ip
        return None

    @classmethod
    def get_visa_instance_fault(cls, name: str) -> dict:
        ret = {"message": "", "code": 0, "details": "",
               "createdAt": ""}
        term_partials = []
        wait_partials = []

        partials = {"message": [], "details": [], "times": []}
        if cls.get_visa_instance_state(name) not in ("ERROR"):
            return ret

        live_object_pod = cls.__get_live_pod_object(name)
        if live_object_pod and live_object_pod.items:
            if hasattr(live_object_pod.items[0], 'status') and hasattr(live_object_pod.items[0].status,
                                                                       'container_statuses'):
                for container_status in live_object_pod.items[0].status.container_statuses:
                    msg, details, date = "", "", ""

                    if not container_status.ready:
                        if hasattr(container_status.state, 'terminated'):
                            c_status_term = container_status.state.terminated
                            if hasattr(c_status_term, 'message'):
                                msg = c_status_term.message
                            if hasattr(c_status_term, 'reason'):
                                details = c_status_term.reason
                            if hasattr(c_status_term, 'finished_at'):
                                date = c_status_term.finished_at
                        term_partials.append((msg, details, date))

                    if hasattr(container_status.state, 'waiting'):
                        c_status_wait = container_status.state.waiting
                        if hasattr(c_status_wait, 'message'):
                            msg = c_status_wait.message
                        if hasattr(c_status_wait, 'reason'):
                            details = c_status_wait.reason
                        if hasattr(c_status_wait, 'finished_at'):
                            date = c_status_wait.finished_at
                        wait_partials.append((msg, details, date))

        for msg, details, date in term_partials:
            if msg or details:
                if ret["code"] == 0:
                    ret["code"] = -1

                partials["message"].append(f"term-{msg}" if msg else "")
                partials["details"].append(f"term-{details}" if details else "")
                if date:
                    partials["times"].append(date)

        for msg, details, date in wait_partials:
            if msg or details:
                if ret["code"] == 0:
                    ret["code"] = -1

                partials["message"].append(f"wait-{msg}" if msg else "empty")
                partials["details"].append(f"wait-{details}" if details else "empty")
                if date:
                    partials["times"].append(date)

        ret["message"] = "_".join(partials["message"])
        ret["details"] = "_".join(partials["details"])

        min_date = get_min_date(partials["times"])
        if min_date:
            ret["createdAt"] = min_date
        return ret

    @classmethod
    def get_visa_instance_state(cls, name: str) -> str:
        if not name or cls.visa_instance_has_fault(name):
            return "ERROR"

        live_object = cls.__get_backend_client().get_live_object(name=name)
        if not live_object:
            return "DELETED"

        last_action = cls.__get_live_object_vcp_last_action(live_object)

        existing_pods = cls.__get_live_pod_object(name)
        pods_amount = len(existing_pods.items) if existing_pods else 0

        spec_replicas = live_object.spec.replicas if hasattr(live_object.spec, 'replicas') else 0
        ready_replicas = live_object.status.ready_replicas if hasattr(live_object.status, 'ready_replicas') else 0
        ready_replicas = 0 if not ready_replicas else ready_replicas

        if pods_amount == 0 and spec_replicas == 0:
            return "STOPPED"

        if ready_replicas >= spec_replicas == pods_amount:
            return "ACTIVE"

        if last_action:
            if last_action == "start" and spec_replicas == 1 and not ready_replicas:
                return "STARTING"
            elif last_action == "stop" and spec_replicas == 0:
                return "STOPPING"
            elif last_action == "reboot" and spec_replicas == 1 and not ready_replicas:
                return "REBOOTING"
        return "UNKNOWN"

    @classmethod
    def create_visa_instance(cls, name: str, image: Image, flavour: Flavour, sec_groups: list[str], metadata: dict,
                             boot_command: str) -> Instance | None:

        owner, visa_uid = None, None
        if "owner" in metadata:
            owner = metadata["owner"]
        if "uid" in metadata:
            visa_uid = metadata["uid"]

        visa_instance = Instance(name=name, flavour=flavour, image=image, active=False, visa_uid=visa_uid)
        visa_instance.save()

        # Add local security groups
        for group in sec_groups:
            try:
                db_group = SecurityGroup.objects.get(name=group)
            except SecurityGroup.DoesNotExist:
                if group.startswith('u'):
                    try:
                        proposal_account = ProposalAccount.objects.get(username=f"{group}")
                        visa_instance.associated_proposals.add(proposal_account)
                    except ProposalAccount.DoesNotExist:
                        pass
                db_group = None
            if db_group:
                visa_instance.security_groups.add(db_group)

        visa_instance.deployment_name = f"{settings.VISA_DEFAULT_DEPLOYMENT_PREFIX}-{str(visa_instance.id)}"
        visa_instance.save()

        selector_labels = {
            "environment": settings.DJANGO_ENV.lower(),
            "component": "visa-user-pod",
            "name": visa_instance.deployment_name,
            "flavour": re.sub('[^0-9a-zA-Z]+', '', visa_instance.flavour.name.lower()),
            "image": re.sub('[^0-9a-zA-Z]+', '', visa_instance.image.name.lower()),
            "owner": owner if owner else "owner-not-received-on-instance-creation",
            "visa-uid": visa_uid if visa_uid else "uid-not-received-on-instance-creation",
        }
        metadata_labels = {
            **selector_labels,
        }

        main_container_ports = cls.__get_main_container_ports(visa_instance)

        volumes, volume_mounts, gids, investigation_paths, scratch_volume_mount = cls.__get_instrument_storage_volumes_mounts_and_gid_values(
            visa_instance)

        tmp_volume = V1Volume(name="shared-tmp-volume", empty_dir=V1EmptyDirVolumeSource())
        tmp_volume_mount = V1VolumeMount(name="shared-tmp-volume", mount_path="/tmp")
        volumes.append(tmp_volume)
        volume_mounts.append(tmp_volume_mount)

        """
        # Removed due to K8s 63 char limit on label fields.
        if gids:
            metadata_labels["proposal-gids"] = "-".join([str(gid) for gid in gids])
        """
        pvc_volume, pvc_volume_mount = cls.__provision_pvc_retrieve_volume_and_mounts(visa_instance)
        if pvc_volume and pvc_volume_mount:
            volumes.append(pvc_volume)
            volume_mounts.append(pvc_volume_mount)

        additional_containers = cls.__get_additional_services_containers(visa_instance, pvc_volume_mount,
                                                                         tmp_volume_mount,
                                                                         scratch_volume_mount)

        container_limits = {"memory": f"{flavour.ram}Mi", "cpu": str(flavour.cpus)}

        visa_pam_key_env_var = V1EnvVar(name="VISA_PAM_PUBLIC_KEY", value=metadata['pamPublicKey'])
        tz_env_var = V1EnvVar(name="TZ", value=settings.VISA_INSTANCE_DEFAULT_TIMEZONE)

        visa_public_key_volume_mount, visa_public_key_config_map_volume = cls.__get_visa_pam_public_key_mount()

        live_object = cls.__get_backend_client().init_live_object(visa_instance.deployment_name, metadata_labels,
                                                                  selector_labels)

        boot_command_str: list = boot_command.split(" ")

        live_object.spec.template.spec = V1PodSpec(
            containers=[
                V1Container(name="visa-instance-container", image=visa_instance.image.full_image_url,
                            image_pull_policy=settings.VISA_DEFAULT_IMAGE_PULL_POLICY,
                            ports=main_container_ports,
                            resources=V1ResourceRequirements(requests=container_limits, limits=container_limits),
                            volume_mounts=[visa_public_key_volume_mount,
                                           *volume_mounts],
                            env=[visa_pam_key_env_var, tz_env_var,
                                 V1EnvVar(name="NODE_FS_API_SERVER_AUTH_TOKEN",
                                          value=str(visa_instance.id)),
                                 V1EnvVar(name="VISA_PRINT_SERVER_AUTH_TOKEN",
                                          value=str(visa_instance.id)),
                                 V1EnvVar(name="VISA_INSTANCE_UID",
                                          value=str(visa_instance.visa_uid))
                                 ],
                            command=[i.strip() for i in boot_command_str] if boot_command else None,
                            lifecycle=cls.__get_container_post_start_lifecycle(
                                visa_instance, [owner], image, sec_groups, supplemental_groups=gids,
                                investigation_paths=investigation_paths)
                            ),
                *additional_containers,
            ],
            volumes=[visa_public_key_config_map_volume, *volumes],
            dns_policy=settings.VISA_DEFAULT_DNS_POLICY
        )

        if gids:
            security_context = V1PodSecurityContext(supplemental_groups=gids)
            live_object.spec.template.spec.security_context = security_context

        if settings.VISA_IMAGE_PULL_SECRET_NAME and settings.VISA_IMAGE_PULL_SECRET_NAMESPACE:
            live_object.spec.template.spec.image_pull_secrets = [
                V1SecretReference(name=settings.VISA_IMAGE_PULL_SECRET_NAME,
                                  namespace=settings.VISA_IMAGE_PULL_SECRET_NAMESPACE)]

        live_object = cls.__get_backend_client().create_live_object(live_object)

        if live_object:
            visa_instance.deployment_representation = json.dumps(live_object.to_dict(), default=str)
            visa_instance.active = True
            visa_instance.save()
            return visa_instance
        return None
