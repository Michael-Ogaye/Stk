

from rest_framework import serializers

from .models import LNM


class LNMSerializer(serializers.ModelSerializer):
    class Meta:
        model =LNM
        fields = ("id")
