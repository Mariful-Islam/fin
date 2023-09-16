from rest_framework.serializers import ModelSerializer
from base.models import *


class TransferSerializer(ModelSerializer):
    class Meta:
        model = Transfer
        fields = "__all__"
