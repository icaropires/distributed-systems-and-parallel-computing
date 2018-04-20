from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Pair
from .serializers import PairSerializer


class PairViewSet(viewsets.ModelViewSet):

    serializer_class = PairSerializer
    queryset = Pair.objects.all()

    @action(methods=['get'], detail=False)
    def pairOut(self, request, pk=None):
        key = request.query_params['key']

        data = None
        if key:
            pair = self.queryset.get(key=key)
            pair = self.serializer_class(pair)

            data = pair.data
        else:
            raise ValueError('An key must be provided')

        return Response(data)
