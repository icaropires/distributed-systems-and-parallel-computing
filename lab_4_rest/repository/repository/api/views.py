from sys import stderr
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Pair
from .serializers import PairSerializer


class PairViewSet(viewsets.ModelViewSet):

    serializer_class = PairSerializer
    queryset = Pair.objects.all()
    response = None

    @action(methods=['get'], detail=False)
    def pairOut(self, request, pk=None):
        response = self._get_get_pair_reponse(request)

        if response.status_code == 200:
            pairs = self.queryset.filter(key=request.query_params['key'])
            pairs.last().delete()

        return response

    @action(methods=['get'], detail=False)
    def readPair(self, request, pk=None):
        response = self._get_get_pair_reponse(request)

        return response

    def _get_get_pair_reponse(self, request):
        try:
            data = self._get_pair_data(request)

            if data:
                response = Response(data, 200)
            else:
                response = Response(None, 404)

        except ValueError:
            print('A key must be provided', file=stderr)
            response = Response(None, 400)

        return response

    def _get_pair_data(self, request):
        key = request.query_params.get('key', None)

        data = None
        if key:
            pair = self.queryset.filter(key=key).last()

            pair_serialized = self.serializer_class(pair)
            data = pair_serialized.data if pair else None
        else:
            raise ValueError('A key must be provided')

        return data
