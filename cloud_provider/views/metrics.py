from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_api_key.permissions import HasAPIKey
from django.conf import settings
from cloud_provider.models import CloudLimit
from cloud_provider.utils.kubernetes.kubernetes_client import KubernetesClient


class MetricsView(GenericAPIView):
    permission_classes = [IsAuthenticated | HasAPIKey]

    def get(self, *args, **kwargs):
        if settings.TESTING_MODE:
            commited_instances, commited_cpu, commited_mib = 0, 0, 0
        else:
            commited_instances, commited_cpu, commited_mib = KubernetesClient.get_commited_resources()

        total_mib_available = float(CloudLimit.objects.get(name="MAX_TOTAL_RAM_ALLOWED").value)
        total_cpu_available = float(CloudLimit.objects.get(name="MAX_TOTAL_CORES_ALLOWED").value)
        total_instances_available = int(CloudLimit.objects.get(name="MAX_INSTANCE_AMOUNT").value)

        ret = {
            "maxTotalRamSize": total_mib_available,
            "totalRamUsed": commited_mib,
            "totalInstancesUsed": commited_instances,
            "maxTotalInstances": total_instances_available,
            "maxTotalCores": total_cpu_available,
            "totalCoresUsed": commited_cpu
        }
        return Response(data=ret, status=status.HTTP_200_OK)
