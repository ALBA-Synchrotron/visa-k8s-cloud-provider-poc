from rest_framework import serializers

from cloud_provider.models import ProposalAccount, StorageConfig


class InstrumentSerializer(serializers.Serializer):
    id = serializers.CharField(required=True)
    name = serializers.CharField(required=True)


class ExperimentsSerializer(serializers.Serializer):
    # The experiments field contains way more attributes than we need. We are only interested in the id / serialNumbers
    # of the proposals selected for a given instance and the instrument the proposal belongs to, we will ignore the rest.
    id = serializers.CharField(required=True)
    instrument = InstrumentSerializer(required=True)


class InstanceSecurityGroupSVCSerializer(serializers.Serializer):
    # The POST method of the security group service receives way more attributes than we need. For now we will only
    # use the ones we need. The rest will be ignored.
    experiments = ExperimentsSerializer(required=True, many=True)

    @staticmethod
    def __validate_experiment_fields__(experiment):
        serial_number = experiment.get("id")
        if not serial_number:
            raise serializers.ValidationError("Experiment id / serial number is required.")
        instrument = experiment["instrument"]
        if not instrument:
            raise serializers.ValidationError("Instrument is required.")
        instrument_name = instrument.get("name")
        if not instrument_name:
            raise serializers.ValidationError("Instrument name is required.")

    @classmethod
    def __validate_experiment_configuration__(cls, experiment):
        serial_number = experiment.get("id")
        instrument_name = experiment.get("instrument").get("name")

        storage_config = StorageConfig.objects.get(instrument=instrument_name)
        if not storage_config:
            # Case storage has not been created in database.
            return None
        if not storage_config.enabled:
            # Case storage has been disabled or not fully configured (e.g. missing NFS export configuration).
            return None
        try:
            proposal_account = ProposalAccount.objects.get(username=f"u{serial_number}")
        except ProposalAccount.DoesNotExist:
            return None

        if len(proposal_account.home_directory_list.all()) == 0:
            # Case proposal account does not have any indicated home directories.
            return None
        return experiment

    def validate(self, attrs) -> list:
        ret = []
        for experiment in attrs["experiments"]:
            self.__class__.__validate_experiment_fields__(experiment)
            ret.append(self.__class__.__validate_experiment_configuration__(experiment))
        return [i for i in ret if i is not None]

    def to_representation(self, instance) -> list:
        return [f"u{experiment.get("id")}" for experiment in instance]
