from django.db import models

class Criacao(models.Model):
  id = models.AutoField(primary_key=True)
  raca = models.TextField(max_length=120)
  data_entrada = models.DateField()

  def __str__(self):
    return self.raca


class Coleta(models.Model):
    id = models.AutoField(primary_key=True)
    criacao = models.ForeignKey(Criacao, on_delete=models.CASCADE)
    data = models.DateField()
    quantidade = models.DecimalField(decimal_places=3, max_digits=12)
