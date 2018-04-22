from sys import stderr
from functools import reduce
import time
from django.core.management.base import BaseCommand, CommandError
from django.core.validators import ValidationError
from rest_framework import status
import requests
from api.models import Matrix


REPOSITORY_BASE_URL = 'http://192.168.182.2:8001/api/'


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        while True:
            print('\n--------------------------------')
            print('Insira a opção desejada. Insira EXIT para sair')
            print('1. Registrar matriz')
            print('2. Multiplicar matrizes')
            selection = input()

            if selection != 'EXIT':
                options = {
                    '1': self.register_matrix,
                    '2': self.multiply_matrixes,
                }

                selected_option = options[selection]
                selected_option()
            else:
                break

    @staticmethod
    def register_matrix():
        name = input('Insira o nome para a matriz: ')

        print('\nInsira a matrix linha por linha')
        print('Separe os elementos por espaço.'
              ' Use uma linha em branco para finalizar a inserção')

        matrix = Command.get_matrix()
        matrix = Command.matrix_to_string(matrix)

        try:
            matrix = Matrix.objects.create(name=name, matrix=matrix)
            print('Matriz registrada com sucesso!')
        except ValidationError:
            CommandError('Não foi possível registrar a matriz')

    def multiply_matrixes(self):
        matrix_a_name, matrix_b_name = self.get_chosen_matrixes()

        try:
            matrix_a = Matrix.objects.get(name=matrix_a_name)
            matrix_b = Matrix.objects.get(name=matrix_b_name)
        except Matrix.DoesNotExists:
            raise CommandError('Invalid names for matrixes')

        if matrix_a.width == matrix_b.height:
            self.upload_matrix(matrix_a.get_matrix(), first_operand=True)
            self.upload_matrix(matrix_b.get_matrix(), first_operand=False)
        else:
            raise AttributeError("Incompatible matrixes for multiplication")

    @staticmethod
    def upload_matrix(matrix, first_operand=True):
        prepared_matrix = []
        prefix_key_name = ''

        if first_operand:
            prepared_matrix = matrix
            prefix_key_name = 'A'
        else:
            prefix_key_name = 'B'
            prepared_matrix = Command.transpose_matrix(matrix)

        url = REPOSITORY_BASE_URL + 'pairIn/'
        for index, vector in enumerate(prepared_matrix):
            Command.post_vector(vector, url, prefix_key_name, index)

    @staticmethod
    def matrix_to_string(matrix):
        matrix = [str(row) for row in matrix]
        matrix = reduce(lambda x, y: x + y, matrix)

        return matrix

    @staticmethod
    def get_matrix():
        matrix = []
        while True:
            row = input()
            if row:
                elements = [int(element) for element in row.split()]
                matrix += [elements]
            else:
                break

        return matrix

    @staticmethod
    def get_chosen_matrixes():
        matrixes_names = [matrix.name for matrix in Matrix.objects.all()]

        print()
        print('Matrizes cadastradas:')
        for matrix in matrixes_names:
            print(matrix)
        print()

        print('Quais matrizes deseja multiplicar?'
              ' Insira o nome de ambas separado por espaços na ordem da'
              ' multiplicação')
        matrix_a, matrix_b = input().split()
        
        return matrix_a, matrix_b

    @staticmethod
    def transpose_matrix(matrix):
        transposed_matrix = []
        for i in range(len(matrix[0])):
            transposed_matrix += [[line[i] for line in matrix]]

        return transposed_matrix

    @staticmethod
    def post_vector(vector, url, prefix_key_name, index):
        pair = {'key': prefix_key_name + str(index), 'value': str(vector)}

        print('Sending term {} to {}... '
              .format(prefix_key_name + str(index), url), end='')

        response = requests.post(url, json=pair)

        if response.status_code == status.HTTP_201_CREATED:
            print('ok')
        else:
            print(
                "Couldn't send term {} from {} matrix! Response: {}"
                .format(index, prefix_key_name, response.content), file=stderr
            )
