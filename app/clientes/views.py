from django.shortcuts import render
from django.http import JsonResponse, HttpResponseNotFound
from django.core import serializers
import re
import json

from .models import Cliente, Carro

def clientes(request):
  if request.method == 'GET':
    clientes = Cliente.objects.all()
    return render(request, 'clientes.html', {'clientes': clientes})
  
  else:
    return HttpResponseNotFound('Not Found')

def cadastrar_cliente(request):
  if request.method == 'GET':
    return render(request, 'adicionar-cliente.html')
  
  elif request.method == 'POST':
    import json
    response_data = {}

    data = json.loads(request.body.decode('utf-8'))
    nome = data.get('nome')
    sobrenome = data.get('sobrenome')
    email = data.get('email')
    cpf = data.get('cpf')

    cliente_bd = Cliente.objects.filter(cpf=cpf)
    if cliente_bd.exists():
      print('Cliente já existe!')
      response_data['result'] = 'error'
      response_data['message'] = 'Cliente já existe!'
      return JsonResponse(response_data)
    
    if not re.fullmatch(re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'), email):
      print('E-mail inválido!')
      response_data['result'] = 'error'
      response_data['message'] = 'E-mail inválido!'
      return JsonResponse(response_data)

    cliente = Cliente(
      nome = nome,
      sobrenome = sobrenome,
      email = email,
      cpf = cpf
    )
    cliente.save()

    carros = data.get('carros')
    for c in carros:
      carro = Carro(
        modelo = c.get('modelo'),
        placa = c.get('placa'),
        ano = c.get('ano'),
        cliente = cliente
      )
      carro.save()

    print(f'Cliente cadastrado: {cliente}')
    
    response_data['result'] = 'success'
    response_data['message'] = f'Cliente cadastrado: {cliente}'
    return JsonResponse(response_data)

  else:
    return HttpResponseNotFound('Not Found')

# @csrf_exempt
def api_cliente(request, id):
  if request.method == 'GET':
    cliente = Cliente.objects.filter(id=id)
    carros = Carro.objects.filter(cliente=cliente[0])
    
    cliente_serialize = serializers.serialize('json', cliente)
    carros_serialize = serializers.serialize('json', carros)
    
    cliente_json = json.loads(cliente_serialize)[0].get('fields')

    carros_json = []
    for carro in json.loads(carros_serialize):
      carro_obj = carro['fields']
      carro_obj['id'] = carro['pk']
      carros_json.append(carro_obj)
    
    return JsonResponse({'cliente': cliente_json, 'carros': carros_json})
  
  if request.method == 'PUT':
    response_data = {}

    data = json.loads(request.body.decode('utf-8'))
    nome = data.get('nome')
    sobrenome = data.get('sobrenome')
    email = data.get('email')
    cpf = data.get('cpf')

    cliente_bd = Cliente.objects.get(id=id)
    if not cliente_bd:
      print('Cliente não localizado!')
      response_data['result'] = 'error'
      response_data['message'] = 'Cliente não localizado!'
      return JsonResponse(response_data)
    
    carros = data.get('carros')

    for carro in carros:
      carro_id = carro.get('carro_id')
      if carro_id:
        valida_placa = Carro.objects.exclude(id=carro.get('carro_id')).filter(placa=carro.get('placa'))
        if valida_placa.exists():
          print(f'Placa do {carro.get("modelo")} já cadastrada em outro carro!')
          response_data['result'] = 'error'
          response_data['message'] = f'Placa do {carro.get("modelo")} já cadastrada em outro carro!'
          return JsonResponse(response_data)
        
        carro_bd = Carro.objects.get(id=carro_id)
        carro_bd.modelo = carro.get('modelo')
        carro_bd.placa = carro.get('placa')
        carro_bd.ano = carro.get('ano')
        carro_bd.save()
      else:
        novo_carro = Carro(
          modelo = carro.get('modelo'),
          placa = carro.get('placa'),
          ano = carro.get('ano'),
          cliente = cliente_bd
        )
        novo_carro.save()
      
    cliente_bd.nome = nome or cliente_bd.nome
    cliente_bd.sobrenome = sobrenome or cliente_bd.sobrenome
    cliente_bd.email = email or cliente_bd.email
    cliente_bd.cpf = cpf or cliente_bd.cpf
    cliente_bd.save()

    response_data['result'] = 'success'
    response_data['message'] = f'Cliente {cliente_bd} atualizado com sucesso!'
    return JsonResponse(response_data)
  
  if request.method == 'DELETE':
    response_data = {}

    response_data['result'] = 'success'
    response_data['message'] = f'Cliente excluído: teste'
    return JsonResponse(response_data)
  
  else:
    return HttpResponseNotFound('Not Found')

def api_carros(request, id):
  if request.method == 'DELETE':
    response_data = {}
    carro_bd = Carro.objects.get(id=id)

    if not carro_bd:
      response_data['result'] = 'error'
      response_data['message'] = 'Carro não encontrado'
      return JsonResponse(response_data)
    
    carro_bd.delete()
    response_data['result'] = 'success'
    response_data['message'] = f'Carro {carro_bd} excluído!'
    return JsonResponse(response_data)

  else:
    return HttpResponseNotFound('Not Found')