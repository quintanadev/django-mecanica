from django.shortcuts import render

def servicos(request):
  if request.method == 'GET':
    return render(request, 'servicos.html', {'servicos': 'teste'})
