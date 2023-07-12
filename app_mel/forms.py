from django.utils import timezone

from django import forms
from django.core.exceptions import ValidationError

from app_mel.models import Coleta


class ColetaForm(forms.ModelForm):
  class Meta:
    model = Coleta
    fields = ['criacao', 'data', 'quantidade']
    widgets = {
      'criacao': forms.Select(attrs={
        'class': 'appearance-none bg-gray-900 text-white border border-gray-700 rounded w-full py-2 px-3 leading-tight focus:outline-none focus:border-blue-500'
      }),
      'data': forms.DateInput(attrs={
        'type': 'date',
        'class': 'appearance-none bg-gray-900 text-white border border-gray-700 rounded w-full py-2 px-3 leading-tight focus:outline-none focus:border-blue-500',
      }),
      'quantidade': forms.NumberInput(attrs={
        'class': 'appearance-none bg-gray-900 text-white border border-gray-700 rounded w-full py-2 px-3 leading-tight focus:outline-none focus:border-blue-500',
        'step': '1',
      }),
    }
  def clean_data(self):
    data = self.cleaned_data['data']
    criacao = self.cleaned_data['criacao']

    # Verifique se existe um objeto Coleta com esta data e criação.
    coletas = Coleta.objects.filter(data=data, criacao=criacao)

    # Se este form tem uma instância (ou seja, estamos atualizando, não criando),
    # e a coleta encontrada é a mesma que a instância atual, ignore.
    if self.instance and coletas.count() == 1 and coletas.first().id == self.instance.id:
      return data

    # Se nenhuma coleta foi encontrada, ou mais de uma foi encontrada, levante um erro.
    if coletas.exists():
      raise forms.ValidationError("Já existe uma coleta registrada nesta data.")

    if data > timezone.now().date():
      raise forms.ValidationError("A data não pode ser no futuro.")

    return data

  def clean(self):
    cleaned_data = super().clean()
    criacao = cleaned_data.get('criacao')
    data = cleaned_data.get('data')

    coletas = Coleta.objects.filter(criacao=criacao, data=data)

    # Mesma lógica que antes, ignorar se a coleta encontrada é a mesma que a instância atual.
    if self.instance and coletas.count() == 1 and coletas.first().id == self.instance.id:
      return cleaned_data

    if coletas.exists():
      raise ValidationError("Já existe uma coleta registrada nesta data.")

    return cleaned_data
