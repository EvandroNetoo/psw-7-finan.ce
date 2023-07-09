from datetime import datetime
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.contrib.messages import constants
from django.contrib import messages
from django.db.models import Sum
from apps.perfil.utils import calcula_equilibrio_financeiro

from extrato.models import Valores

from .models import Categoria, Conta


def home(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        contas = Conta.objects.all()
        valor_total = f'{contas.aggregate(Sum("valor"))["valor__sum"]:.2f}'.replace('.', ',')
        
        valores = Valores.objects.filter(data__month=datetime.now().month)
        entradas = valores.filter(tipo='E')
        saidas = valores.filter(tipo='S')

        total_entradas = f'{entradas.aggregate(Sum("valor"))["valor__sum"]:.2f}'.replace('.', ',') \
                        if entradas.aggregate(Sum("valor"))["valor__sum"] \
                        else '0,00'
                        
        total_saidas = f'{saidas.aggregate(Sum("valor"))["valor__sum"]:.2f}'.replace('.', ',') \
                        if saidas.aggregate(Sum("valor"))["valor__sum"] \
                        else '0,00'
                        
        percentual_gastos_essenciais, percentual_gastos_nao_essenciais = calcula_equilibrio_financeiro()
        print(calcula_equilibrio_financeiro())
        return render(request, 'home.html', {'contas': contas,
                                             'valor_total': valor_total,
                                             'total_entradas': total_entradas,
                                             'total_saidas': total_saidas,
                                             'percentual_gastos_essenciais': percentual_gastos_essenciais,
                                             'percentual_gastos_nao_essenciais': percentual_gastos_nao_essenciais,
                                             })


def gerenciar(request: HttpRequest) -> HttpResponse:
    contas = Conta.objects.all()
    valor_total = f'{contas.aggregate(Sum("valor"))["valor__sum"]:.2f}'.replace('.', ',')
    categorias = Categoria.objects.all()
    return render(request, 'gerenciar.html', {'contas': contas,
                                              'valor_total': valor_total,
                                              'categorias': categorias
                                              })


def cadastrar_banco(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        apelido = request.POST.get('apelido')
        banco = request.POST.get('banco')
        tipo = request.POST.get('tipo')
        valor = request.POST.get('valor')
        icone = request.FILES.get('icone')
        
        if len(apelido.strip()) == 0 or len(valor.strip()) == 0:
            messages.add_message(request, constants.ERROR, 'Preencha todos os campos.')
            return redirect('gerenciar')
        
        conta = Conta(
            apelido = apelido,
            banco=banco,
            tipo=tipo,
            valor=valor,
            icone=icone
        )
        conta.save()
        
        messages.add_message(request, constants.SUCCESS, 'Conta cadastrada com sucesso.')
        return redirect('gerenciar')
    
    
def deletar_banco(request: HttpRequest, id: int) -> HttpResponse:
    if request.method == 'GET':
        Conta.objects.get(id=id).delete()
        messages.add_message(request, constants.SUCCESS, 'Conta excluida com sucesso.')
        return redirect('gerenciar')
    
    
def cadastrar_categoria(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        nome = request.POST.get('categoria')
        essencial = bool(request.POST.get('essencial'))

        if nome.strip() == '':
            messages.add_message(request, constants.ERROR, 'Preencha todos os campos.')
            return redirect('gerenciar')

        categoria = Categoria(
            categoria=nome,
            essencial=essencial
        )

        categoria.save()

        messages.add_message(request, constants.SUCCESS, 'Categoria cadastrada com sucesso')
        return redirect('gerenciar')
    
    
def update_categoria(request: HttpRequest, id: int) -> HttpResponse:
    categoria = Categoria.objects.get(id=id)

    categoria.essencial = not categoria.essencial

    categoria.save()

    return redirect('gerenciar')