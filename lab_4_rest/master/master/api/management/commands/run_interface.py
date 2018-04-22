from sys import stderr
from functools import reduce
import time
from django.core.management.base import BaseCommand, CommandError
from django.core.validators import ValidationError
from rest_framework import status
import requests
from api.models import Matrix


REPOSITORY_BASE_URL = 'http://192.168.182.5:8001/api/'


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        while True:
            print('\n-----------------------------------------------')
            print('Insira a opção desejada:')
            print('1. Registrar matriz')
            print('2. Multiplicar matrizes')
            print('Qualquer outra coisa para sair')

            selection = input()
            options = {
                '1': self.register_matrix,
                '2': self.multiply_matrixes,
            }

            selected_option = options.get(selection, None)

            if selected_option is not None:
                selected_option()
            else:
                print('\nSaindo...')
                print('-----------------------------------------------')
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

    @staticmethod
    def multiply_matrixes():
        matrix_a_name, matrix_b_name = Command.get_chosen_matrixes()

        try:
            matrix_a = Matrix.objects.get(name=matrix_a_name)
            matrix_b = Matrix.objects.get(name=matrix_b_name)
        except Matrix.DoesNotExists:
            raise CommandError('Invalid names for matrixes')

        print()
        if matrix_a.width == matrix_b.height:
            Command.upload_matrix(matrix_a, first_operand=True)
            Command.upload_matrix(matrix_b, first_operand=False)
        else:
            raise AttributeError("Incompatible matrixes for multiplication")

        print()
        Command.upload_tasks(matrix_a, matrix_b)

    @staticmethod
    def upload_matrix(matrix, first_operand=True):
        prepared_matrix, prefix_key_name = [], ''

        if first_operand:
            prefix_key_name = 'A'
            prepared_matrix = matrix.get_matrix()
        else:
            prefix_key_name = 'B'
            prepared_matrix = Command.transpose_matrix(matrix.get_matrix())

        url_pair_in = REPOSITORY_BASE_URL + 'pairIn/'
        for index, vector in enumerate(prepared_matrix):
            Command.post_vector(vector, url_pair_in, prefix_key_name, index)

    @staticmethod
    def upload_tasks(matrix_a, matrix_b):
        for i in range(matrix_a.height):
            for j in range(matrix_b.width):
                Command.addTask(i, j)

    @staticmethod
    def addTask(i, j):
        url = REPOSITORY_BASE_URL + 'pairIn/'
        pair = {'key': 'Next Task', 'value': '{},{}'.format(i, j)}

        print('Sending task ({},{}) to {} ... '.format(i, j, url), end='')
        response = requests.post(url, json=pair)

        if response.status_code == status.HTTP_201_CREATED:
            print('ok')
        else:
            raise CommandError("Couldn't add task to repository. Response {}"
                               .format(response.text))

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
        vector_name = prefix_key_name + str(index)

        print('Sending vector {} to {} ... '.format(vector_name, url), end='')

        response = requests.post(url, json=pair)

        if response.status_code == status.HTTP_201_CREATED:
            print('ok')
        else:
            print("Couldn't send vector {}! Response: {}"
                  .format(vector_name, response.text), file=stderr)
