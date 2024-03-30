from django.db import models
from datetime import datetime
from app.clientes.models import Cliente
from .choices import ChoicesStatus

class Categoria(models.Model):
  descricao = models.CharField(max_length=50)
  preco = models.DecimalField(max_digits=8, decimal_places=2)

  def __str__(self) -> str:
    return self.descricao

class Servico(models.Model):
  descricao = models.CharField(max_length=100)
  protocolo = models.CharField(max_length=20, null=True, blank=True, editable=False)
  cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
  data_inicio = models.DateField()
  data_previsao = models.DateField(null=True, blank=True)
  data_entrega = models.DateField(null=True, blank=True)
  categoria = models.ManyToManyField(Categoria)
  status = models.CharField(max_length=50, choices=ChoicesStatus.choices, default='criado')
  flag_finalizado = models.BooleanField(default=False)

  def __str__(self) -> str:
    return self.descricao
  
  def save(self, *args, **kwargs):
    if not self.protocolo:
      self.protocolo = datetime.now().strftime('%Y%m%d%H%M%S%f')
    super(Servico, self).save(*args, **kwargs)

  def preco_servico(self):
    preco = float(0)
    for categoria in self.categoria.all():
      preco += float(categoria.preco)
    return preco