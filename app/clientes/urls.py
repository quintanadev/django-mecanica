from django.urls import path
from . import views

urlpatterns = [
  path('', views.clientes, name='clientes'),
  path('<int:id>/', views.api_cliente, name='api-cliente'),
  path('cadastrar/', views.cadastrar_cliente, name='cadastrar-cliente'),
  path('carros/<int:id>/', views.api_carros, name='api-carros'),
]