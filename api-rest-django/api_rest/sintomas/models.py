from django.db import models

class Sintoma(models.Model):
    sintoma1 = models.CharField(max_length=255)
    sintoma2 = models.CharField(max_length=255)
    sintoma3 = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.sintoma1}, {self.sintoma2}, {self.sintoma3}"