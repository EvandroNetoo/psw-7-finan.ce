from datetime import datetime
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.messages import constants
from django.db.models import Sum

from perfil.models import Categoria

from extrato.models import Valores

from .models import ContaPagar, ContaPaga


def definir_contas(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        categorias = Categoria.objects.all()
        return render(request, 'definir_contas.html', {'categorias': categorias})

    elif request.method == 'POST':
        titulo = request.POST.get('titulo')
        categoria = request.POST.get('categoria')
        descricao = request.POST.get('descricao')
        valor = request.POST.get('valor')
        dia_pagamento = request.POST.get('dia_pagamento')

        conta = ContaPagar(
            titulo=titulo,
            categoria_id=categoria,
            descricao=descricao,
            valor=valor,
            dia_pagamento=dia_pagamento
        )

        conta.save()

        messages.add_message(request, constants.SUCCESS,
                             'Conta cadastrada com sucesso')
        return redirect('definir_contas')


def ver_contas(request):
    MES_ATUAL = datetime.now().month
    DIA_ATUAL = datetime.now().day

    contas = ContaPagar.objects.all()

    contas_pagas = ContaPaga.objects.filter(
        data_pagamento__month=MES_ATUAL).values('conta')

    contas_vencidas = contas.filter(
        dia_pagamento__lt=DIA_ATUAL).exclude(id__in=contas_pagas)

    contas_proximas_vencimento = contas.filter(
        dia_pagamento__lte=DIA_ATUAL + 5).filter(dia_pagamento__gte=DIA_ATUAL).exclude(id__in=contas_pagas)

    restantes = contas.exclude(id__in=contas_vencidas).exclude(
        id__in=contas_pagas).exclude(id__in=contas_proximas_vencimento)

    return render(request, 'ver_contas.html', {'contas_vencidas': contas_vencidas,
                                               'contas_proximas_vencimento': contas_proximas_vencimento,
                                               'restantes': restantes})


def dashboard(request):
    dados = {}
    categorias = Categoria.objects.all()

    for categoria in categorias:
        dados[categoria.categoria] = Valores.objects.filter(categoria=categoria).aggregate(Sum('valor'))['valor__sum']

    return render(request, 'dashboard.html', {'labels': list(dados.keys()), 'values': list(dados.values())})