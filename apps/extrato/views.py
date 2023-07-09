from datetime import datetime
from io import BytesIO
from django.conf import settings
from django.http import FileResponse, HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.messages import constants
from django.template.loader import render_to_string
from weasyprint import HTML
from perfil.models import Conta, Categoria

from .models import Valores


def novo_valor(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        contas = Conta.objects.all()
        categorias = Categoria.objects.all()
        return render(request, 'novo_valor.html', {'contas': contas, 'categorias': categorias})

    elif request.method == 'POST':
        valor = request.POST.get('valor')
        categoria = request.POST.get('categoria')
        descricao = request.POST.get('descricao')
        data = request.POST.get('data')
        conta = request.POST.get('conta')
        tipo = request.POST.get('tipo')

        if '' in [value.strip() for value in request.POST.values()]:
            messages.add_message(request, constants.ERROR,
                                 'Preencha todos os campos.')
            return redirect('novo_valor')

        valores = Valores(
            valor=valor,
            categoria_id=categoria,
            descricao=descricao,
            data=data,
            conta_id=conta,
            tipo=tipo,
        )

        valores.save()

        conta = Conta.objects.get(id=conta)

        if tipo == 'E':
            conta.valor += int(valor)
        else:
            conta.valor -= int(valor)

        conta.save()

        messages.add_message(request, constants.SUCCESS, 'Entrada/Saída cadastrada com sucesso')
        return redirect('novo_valor')


def extrato(request: HttpRequest) -> HttpResponse:
    contas = Conta.objects.all()
    categorias = Categoria.objects.all()
    valores = Valores.objects.filter(data__month=datetime.now().month)

    conta_get = request.GET.get('conta')
    categoria_get = request.GET.get('categoria')

    if conta_get:
        valores = valores.filter(conta__id=conta_get)
    if categoria_get:
        valores = valores.filter(categoria__id=categoria_get)

    return render(request, 'view_extrato.html', {'valores': valores, 'contas': contas, 'categorias': categorias})


def exportar_extrato(request):
    valores = Valores.objects.filter(data__month=datetime.now().month)
    contas = Conta.objects.all()
    categorias = Categoria.objects.all()
    
    path_output = BytesIO()

    template_render = render_to_string('partials/extrato.html', {'valores': valores, 'contas': contas, 'categorias': categorias})
    HTML(string=template_render).write_pdf(path_output)

    path_output.seek(0)
    

    return FileResponse(path_output, filename="extrato.pdf")
    