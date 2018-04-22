from rest_framework import serializers
from .models import Matrix


class MatrixSerializer(serializers.ModelSerializer):

    class Meta:
        model = Matrix
        fields = [
            'name',
            'matrix'
        ]
