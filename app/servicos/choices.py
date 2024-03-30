from django.db.models import TextChoices

class ChoicesStatus(TextChoices):
  CRIADO = 'criado', 'Serviço criado'
  ORCAMENTO = 'orcamento', 'Serviço em fase de orçamento'
  APROVACAO = 'aprovacao', 'Serviço aguardando aprovação do orçamento pelo cliente'
  INICIADO = 'iniciado', 'Serviço iniciado'
  AGUARDANDO = 'aguardando', 'Serviço aguardando outros fatores para continuidade'
  VALIDACAO = 'validacao', 'Serviço em validação pelo cliente'
  FINALIZADO = 'finalizado', 'Serviço finalizado'
