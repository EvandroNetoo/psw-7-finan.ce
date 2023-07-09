from datetime import datetime
from django.db import models

class Categoria(models.Model):
    categoria = models.CharField(max_length=50)
    essencial = models.BooleanField(default=False)
    valor_planejamento = models.FloatField(default=0)

    def __str__(self):
        return self.categoria
    
    def get_valor_planejamento(self):
        return f'{self.valor_planejamento:.2f}'
    
    def get_valor_planejamento_formatado(self):
        return f'{self.valor_planejamento:.2f}'.replace('.', ',')
    
    def total_gasto(self):
        from extrato.models import Valores
        valores = Valores.objects.filter(categoria__id = self.id, data__month=datetime.now().month, tipo='S').aggregate(models.Sum('valor'))
        return f'{valores["valor__sum"]:.2f}'.replace('.', ',') if valores['valor__sum'] else 0

    def percentual_gasto(self):
        try:
            return int(float(self.total_gasto().replace(',', '.')) / self.valor_planejamento * 100)
        except:
            return 0

class Conta(models.Model):
    banco_choices = (
        ('NU', 'Nubank'),
        ('CE', 'Caixa econômica'),
        ('PP', 'PicPay'),
    )

    tipo_choices = (
        ('pf', 'Pessoa física'),
        ('pj', 'Pessoa jurídica'),
    )

    apelido = models.CharField(max_length=50)
    banco = models.CharField(max_length=2, choices=banco_choices)
    tipo = models.CharField(max_length=2, choices=tipo_choices)
    valor = models.FloatField()
    icone = models.ImageField(upload_to='icones')

    def get_valor_formatado(self):
        return f'{self.valor:.2f}'.replace('.', ',')

    def __str__(self):
        return self.apelido