from sys import stderr
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Pair
from .serializers import PairSerializer


class PairViewSet(viewsets.ModelViewSet):

    serializer_class = PairSerializer
    queryset = Pair.objects.all()

    @action(methods=['get'], detail=False)
    def pairOut(self, request, pk=None):
        response = self._get_get_pair_reponse(request)

        if response.status_code == status.HTTP_200_OK:
            pairs = self.queryset.filter(key=request.query_params['key'])
            pairs.last().delete()

        return response

    @action(methods=['get'], detail=False)
    def readPair(self, request, pk=None):
        response = self._get_get_pair_reponse(request)

        return response

    @action(methods=['post'], detail=False)
    def pairIn(self, request, pk=None):
        data = request.data
        serialized_data = self.serializer_class(data=data)

        if serialized_data.is_valid():
            serialized_data.save()
            return Response({'status': data}, status.HTTP_201_CREATED)

        return Response(serialized_data.errors, status.HTTP_400_BAD_REQUEST)

    @action(methods=['delete'], detail=False)
    def cleanDatabase(self, request, pk=None):
        for pair in Pair.objects.all():
            pair.delete()

        return Response({'status': 'cleaned!'}, status.HTTP_204_NO_CONTENT)

    def _get_get_pair_reponse(self, request):
        try:
            data = self._get_pair_data(request)

            if data:
                response = Response(data, status.HTTP_200_OK)
            else:
                response = Response(None, status.HTTP_404_NOT_FOUND)

        except ValueError:
            print('A key must be provided', file=stderr)
            response = Response(None, status.HTTP_400_BAD_REQUEST)

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
