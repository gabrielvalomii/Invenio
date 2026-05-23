from django.db import models

class User(models.Model):
    nome = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    CNPJ = models.CharField(max_length=18, unique=True)
    senha= models.CharField(max_length=255)
    
    def __str__(self):
        return f"({self.nome}, {self.CNPJ})"
