import requests
import os
from functools import wraps


HTTP_404_NOT_FOUND = 404
HTTP_200_OK = 200
HTTP_201_CREATED = 201


class Slave:

    def __init__(self, url):
        self.base_url = url

    def process_task(self, task):
        coordinates = self._get_task_coordinates(task)

        vector_a, vector_b = self._get_vectors(coordinates)
        result = self._multiply_vectors(vector_a, vector_b)

        self._post_result(coordinates, result)

    def fetch_next_task(self):
        url = self.base_url + 'pairOut/?key=Next+Task'

        print('PID {}: Getting next task ... '.format(os.getpid()), end='')
        response = requests.get(url)

        if response.status_code in (HTTP_200_OK, HTTP_404_NOT_FOUND):
            task = ''
            if response.status_code == HTTP_200_OK:
                print('ok')
                task = response.json()
            else:
                print('Not found')
        else:
            raise AttributeError("Couldn't fetch next task. Response: {}"
                                 .format(response.text))

        return task, response.status_code

    def _post_result(self, coordinates, result):
        url = self.base_url + 'pairIn/'

        key = 'Element' + str(coordinates[0]) + str(coordinates[1])
        pair = {'key': key, 'value': result}

        print('PID {}: Sending result {} to {} ... '
              .format(os.getpid(), key, url), end='')
        response = requests.post(url, json=pair)

        if response.status_code == HTTP_201_CREATED:
            print('ok')
        else:
            raise AttributeError("Couldn't send result!. Response: {}"
                                 .format(response.text))

    @staticmethod
    def _multiply_vectors(vector_a, vector_b):
        assert len(vector_a) == len(vector_b)

        result_sum = 0
        for i, _ in enumerate(vector_a):
            result_sum += vector_a[i] * vector_b[i]

        return result_sum

    def _get_vectors(self, coordinates):
        string_vector_a = self._fetch_vector(coordinates[0],
                                             first_operand=True)
        string_vector_b = self._fetch_vector(coordinates[1],
                                             first_operand=False)

        vector_a = self._get_object_vector(string_vector_a)
        vector_b = self._get_object_vector(string_vector_b)

        return vector_a, vector_b

    @staticmethod
    def _get_task_coordinates(task):
        _, coordinates = Slave._parse_task(task)

        return coordinates

    @staticmethod
    def _get_object_vector(string_vector):
        vector = string_vector[1:-1].split(',')
        vector = list(map(int, vector))

        return vector

    @staticmethod
    def _parse_task(task):
        key = task['key']
        coordinates = list(map(int, task['value'].split(',')))

        return key, coordinates

    def _get_vector_url(self, index, first_operand=True):
        url = self.base_url + 'readPair/?key={}' + str(index)
        url = url.format('A') if first_operand else url.format('B')

        return url

    def _fetch_vector(self, index, first_operand=True):
        vector_url = self._get_vector_url(index, first_operand)
        response = requests.get(vector_url)

        print('PID {}: Getting vector {} ...'
              .format(os.getpid(), vector_url[-2:]), end='')
        if response.status_code == HTTP_200_OK:
            print('ok')
        else:
            raise AttributeError("Couldn't fetch vector. Response: {}"
                                 .format(response.text))

        string_vector = response.json()['value']
        return string_vector
