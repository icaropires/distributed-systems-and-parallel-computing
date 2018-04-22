from sys import stderr
from functools import reduce
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
            print('3. Limpar banco de matrizes')
            print('4. Limpar dados do repositório')
            print('Qualquer outra coisa para sair')

            selection = input()
            options = {
                '1': self.register_matrix,
                '2': self.multiply_matrixes,
                '3': self.clean_local_database,
                '4': self.clean_repository,
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

        matrix = Command._get_matrix()
        matrix = Command._matrix_to_string(matrix)

        try:
            matrix = Matrix.objects.create(name=name, matrix=matrix)
            print('Matriz registrada com sucesso!')
        except ValidationError:
            CommandError('Não foi possível registrar a matriz')

    @staticmethod
    def multiply_matrixes():
        matrix_a_name, matrix_b_name = Command._get_chosen_matrixes()

        try:
            matrix_a = Matrix.objects.get(name=matrix_a_name)
            matrix_b = Matrix.objects.get(name=matrix_b_name)
        except Matrix.DoesNotExists:
            raise CommandError('Invalid names for matrixes')

        print()
        if matrix_a.width == matrix_b.height:
            Command._upload_matrix(matrix_a, first_operand=True)
            Command._upload_matrix(matrix_b, first_operand=False)
        else:
            raise AttributeError("Incompatible matrixes for multiplication")

        print()
        Command._upload_tasks(matrix_a, matrix_b)

        result_matrix = Command._gather_result_matrix(
            matrix_a.height, matrix_b.width
        )

        print()
        print('============================================================')
        print('MATRIX RESULTADO')
        print('============================================================')
        Command._print_matrix(result_matrix)
        print('------------------------------------------------------------')

    @staticmethod
    def clean_local_database():
        for matrix in Matrix.objects.all():
            matrix.delete()

        print('Local database cleaned')

    @staticmethod
    def clean_repository():
        url = REPOSITORY_BASE_URL + 'cleanDatabase/'
        response = requests.delete(url)

        if response.status_code == status.HTTP_204_NO_CONTENT:
            print('\nRepository cleaned successfully!')
        else:
            raise AttributeError("Couldn't clean repository")

    @staticmethod
    def _gather_result_matrix(width, height):
        missing_elements = ['Element' + str(i) + str(j) for i in
                            range(height) for j in range(width)]

        result_matrix, k = [['-'] * width for _ in range(height)], 0

        while missing_elements:
            result, status_code = Command._receive_result(missing_elements[k])

            if status_code != status.HTTP_404_NOT_FOUND:
                i, j = int(result['key'][-2]), int(result['key'][-1])
                result_matrix[i][j] = result['value']

                del missing_elements[k]
                Command._print_matrix(result_matrix)

            k = k + 1 if k < len(missing_elements) - 1 else 0

        return result_matrix

    @staticmethod
    def _print_matrix(matrix):
        for line in matrix:
            print(line)

    @staticmethod
    def _receive_result(element_name):
        url = REPOSITORY_BASE_URL + 'pairOut/?key=' + element_name

        i, j = int(url[-1]), int(url[-2])
        print('\nGetting element ({}, {}) result... '.format(i, j), end='')
        response = requests.get(url)

        result = None
        if (response.status_code in
                (status.HTTP_200_OK, status.HTTP_404_NOT_FOUND)):
            if response.status_code == status.HTTP_200_OK:
                result = response.json()
                print('ok')
            else:
                print('Not Found')
        else:
            raise CommandError("Couldn't get result.")

        return result, response.status_code

    @staticmethod
    def _upload_matrix(matrix, first_operand=True):
        prepared_matrix, prefix_key_name = [], ''

        if first_operand:
            prefix_key_name = 'A'
            prepared_matrix = matrix.get_matrix()
        else:
            prefix_key_name = 'B'
            prepared_matrix = Command._transpose_matrix(matrix.get_matrix())

        url_pair_in = REPOSITORY_BASE_URL + 'pairIn/'
        for index, vector in enumerate(prepared_matrix):
            Command._post_vector(vector, url_pair_in, prefix_key_name, index)

    @staticmethod
    def _upload_tasks(matrix_a, matrix_b):
        for i in range(matrix_a.height):
            for j in range(matrix_b.width):
                Command._addTask(i, j)

    @staticmethod
    def _addTask(i, j):
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
    def _matrix_to_string(matrix):
        matrix = [str(row) for row in matrix]
        matrix = reduce(lambda x, y: x + y, matrix)

        return matrix

    @staticmethod
    def _get_matrix():
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
    def _get_chosen_matrixes():
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
    def _transpose_matrix(matrix):
        transposed_matrix = []
        for i in range(len(matrix[0])):
            transposed_matrix += [[line[i] for line in matrix]]

        return transposed_matrix

    @staticmethod
    def _post_vector(vector, url, prefix_key_name, index):
        pair = {'key': prefix_key_name + str(index), 'value': str(vector)}
        vector_name = prefix_key_name + str(index)

        print('Sending vector {} to {} ... '.format(vector_name, url), end='')

        response = requests.post(url, json=pair)

        if response.status_code == status.HTTP_201_CREATED:
            print('ok')
        else:
            print("Couldn't send vector {}! Response: {}"
                  .format(vector_name, response.text), file=stderr)
