from datetime import datetime
from extrato.models import Valores
from django.db.models import Sum


def calcula_equilibrio_financeiro():
    gastos_essenciais = Valores.objects.filter(data__month=datetime.now().month).filter(tipo='S').filter(categoria__essencial=True)
    gastos_nao_essenciais = Valores.objects.filter(data__month=datetime.now().month).filter(tipo='S').filter(categoria__essencial=False)

    total_gastos_essenciais = gastos_essenciais.aggregate(Sum("valor"))["valor__sum"]
    total_gastos_nao_essenciais = gastos_nao_essenciais.aggregate(Sum("valor"))["valor__sum"]

    total = total_gastos_essenciais + total_gastos_nao_essenciais
    try:
        percentual_gastos_essenciais = total_gastos_essenciais * 100 / total
        percentual_gastos_nao_essenciais = total_gastos_nao_essenciais * 100 / total

        return int(percentual_gastos_essenciais), int(percentual_gastos_nao_essenciais)
    except:
        return 0, 0