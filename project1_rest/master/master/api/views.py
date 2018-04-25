from rest_framework import viewsets, status
from .models import Matrix
from .serializers import MatrixSerializer


class MatrixViewSet(viewsets.ModelViewSet):

    queryset = Matrix.objects.all()
    serializer_class = MatrixSerializer
