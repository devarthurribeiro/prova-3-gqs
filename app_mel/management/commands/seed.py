# app_mel/management/commands/seed.py

from django.core.management.base import BaseCommand
from app_mel.models import Criacao, Coleta
from datetime import date, timedelta
import random

class Command(BaseCommand):
  help = 'Cria dados iniciais para o aplicativo'

  def handle(self, *args, **options):
    self.stdout.write('Criando dados iniciais...')

    # limpar os dados existentes
    Criacao.objects.all().delete()
    Coleta.objects.all().delete()

    racas = ['Apis mellifera', 'Bombus terrestris', 'Megachile rotundata']
    for i in range(3):
      criacao = Criacao.objects.create(raca=racas[i], data_entrada=date.today()-timedelta(days=i*10))
      for j in range(10):
        Coleta.objects.create(
          criacao=criacao,
          data=date.today()-timedelta(days=j*3),
          quantidade=random.uniform(0.5, 2.0)
        )
    self.stdout.write('Dados iniciais criados com sucesso!')
