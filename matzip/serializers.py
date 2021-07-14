from rest_framework import serializers
from .models import Matzip


class MatzipSerializer(serializers.ModelSerializer):

    class Meta:
        model = Matzip
        fields = "__all__"
