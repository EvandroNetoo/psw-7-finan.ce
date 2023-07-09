import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from perfil.models import Categoria


def definir_planejamento(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        categorias = Categoria.objects.all()
        
        return render(request, 'definir_planejamento.html', {'categorias': categorias})


@csrf_exempt
def update_valor_categoria(request: HttpRequest, id: int) -> HttpResponse:
    novo_valor = json.load(request)['novo_valor'].replace(',', '.')
    categoria = Categoria.objects.get(id=id)
    categoria.valor_planejamento = novo_valor
    categoria.save()

    return JsonResponse({'status': 'Sucesso'})


def ver_planejamento(request):
    categorias = Categoria.objects.all()
    return render(request, 'ver_planejamento.html', {'categorias': categorias})
