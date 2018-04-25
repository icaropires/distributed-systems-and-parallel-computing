from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import Matrix, validate_matrix


class MatrixTests(TestCase):

    def setUp(self):
        self.valid_string_matrix = '[1,2][1,2][1,2]'
        self.invalid_string_matrix = '[1,2,3][1, 2][1,2,3]'

    def test_width(self):
        matrix = Matrix.objects.create(matrix=self.valid_string_matrix)
        self.assertEqual(2, matrix.width)

    def test_height(self):
        matrix = Matrix.objects.create(matrix=self.valid_string_matrix)
        self.assertEqual(3, matrix.height)

    def test_get_object_matrix(self):
        valid_object_matrix = [[1, 2], [1, 2], [1, 2]]

        self.assertEqual(
            valid_object_matrix,
            Matrix.get_object_matrix(self.valid_string_matrix)
        )

    def test_validate_matrix(self):
        # Pass if not raises exceptions
        validate_matrix(self.valid_string_matrix)

    def test_validate_matrix_invalid(self):
        invalid_string_matrix_formats = [
            '[1,2,3],[1,2,3]',
            '1,2,3][1,2,3]',
            '[1,2,3]1,2,3]',
            '1,2,3 1,2,3',
            '[1.2.3][1.2.3]',
            '[1,2,3][1,2,3,]',
        ]

        for invalid_matrix in invalid_string_matrix_formats:
            with self.assertRaises(ValidationError):
                validate_matrix(invalid_matrix)

    def test_save_run_validators(self):
        with self.assertRaises(ValidationError):
            Matrix.objects.create(matrix=self.invalid_string_matrix)
