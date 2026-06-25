from rest_framework import status
from rest_framework.response import Response
from django.conf import settings
from cloud_provider.models import CloudLimit
from cloud_provider.utils.kubernetes.kubernetes_client import KubernetesClient


def check_instance_quota():
    if settings.TESTING_MODE:
        return None

    commited_instances, commited_cpu, commited_mib = KubernetesClient.get_commited_resources()

    total_mib_available = float(CloudLimit.objects.get(name="MAX_TOTAL_RAM_ALLOWED").value)
    total_cpu_available = float(CloudLimit.objects.get(name="MAX_TOTAL_CORES_ALLOWED").value)
    total_instances_available = int(CloudLimit.objects.get(name="MAX_INSTANCE_AMOUNT").value)

    if commited_instances >= total_instances_available:
        return Response(data={"message": "Max number of concurrent VISA instances running has been reached"},
                        status=status.HTTP_401_UNAUTHORIZED)

    if commited_mib >= total_mib_available:
        return Response(data={"message": "Max number of allocated RAM for VISA instances has been reached"},
                        status=status.HTTP_401_UNAUTHORIZED)
    if commited_cpu >= total_cpu_available:
        return Response(data={"message": "Max number of allocated CPUs for VISA instances has been reached"},
                        status=status.HTTP_401_UNAUTHORIZED)
    return None
