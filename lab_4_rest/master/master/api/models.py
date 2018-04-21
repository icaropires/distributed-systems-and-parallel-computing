from django.db import models
from django.core.exceptions import ValidationError

# (100 elements + 2 brackets) per row * 100 rows
MATRIX_SIZE = 10200


def validate_matrix(string_matrix):
    validation_exception = ValidationError(
        'This is not a valid matrix.'
        ' It should match the format: [a1, a2, a3][b1, b2, b3]'
    )

    matrix = None
    try:
        matrix = Matrix.get_object_matrix(string_matrix)
    except ValueError:
        raise validation_exception

    line_size = len(matrix[0])
    for line in matrix:
        if len(line) != line_size:
            raise validation_exception


class Matrix(models.Model):

    matrix = models.CharField(
        max_length=MATRIX_SIZE,
        validators=[validate_matrix]
    )

    def get_matrix(self):
        return self.get_object_matrix(self.matrix)

    @property
    def width(self):
        matrix = self.get_matrix()
        return len(matrix[0])

    @property
    def height(self):
        matrix = self.get_matrix()
        return len(matrix)

    @staticmethod
    def get_object_matrix(string_matrix):
        string_matrix = string_matrix.split('][')

        string_matrix[0] = string_matrix[0][1:]
        string_matrix[-1] = string_matrix[-1][:-1]

        matrix = []
        for line in string_matrix:
            row = []
            for element in line.split(','):
                # Will raise ValueError if not correct format
                row += [int(element.strip())]
            matrix += [row]

        return matrix

    def save(self, *args, **kwargs):
        self.full_clean()  # Run validators

        super(Matrix, self).save(*args, **kwargs)
