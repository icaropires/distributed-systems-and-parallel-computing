from django.db import models

# (100 elements + 2 brackets) per row * 100 rows
MAX_MATRIX_SIZE = 10200


class Pair(models.Model):

    key = models.CharField(max_length=100)

    value = models.CharField(max_length=MAX_MATRIX_SIZE)
