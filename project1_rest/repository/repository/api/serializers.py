from rest_framework import serializers
from django.shortcuts import render
from .models import Pair


class PairSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pair
        fields = [
            'key',
            'value'
        ]
