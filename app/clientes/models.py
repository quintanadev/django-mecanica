from django.db import models

class Cliente(models.Model):
  nome = models.CharField(max_length=50)
  sobrenome = models.CharField(max_length=100)
  email = models.CharField(max_length=100)
  cpf = models.CharField(max_length=11)

  def __str__(self) -> str:
    return f'{self.nome} {self.sobrenome}'
  
class Carro(models.Model):
  modelo = models.CharField(max_length=50)
  placa = models.CharField(max_length=10)
  ano = models.IntegerField()
  cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
  qtd_lavagens = models.IntegerField(default=0)
  qtd_consertos = models.IntegerField(default=0)

  def __str__(self) -> str:
    return f'{self.modelo} ({self.placa})'