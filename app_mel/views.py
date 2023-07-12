from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Sum
from django.utils import timezone
from app_mel.forms import ColetaForm
from app_mel.models import Coleta, Criacao
from django.db.models.functions import TruncMonth, ExtractMonth

def relatorio_coleta(request):
  # Número de coletas
  numero_coletas = Coleta.objects.count()

  # Maior coleta e menor coleta
  maior_coleta = Coleta.objects.order_by('-quantidade').first()
  menor_coleta = Coleta.objects.order_by('quantidade').first()


# Quantidade coletada nos últimos 12 meses
  today = timezone.now().date()
  start_date = today - timezone.timedelta(days=365)
  quantidade_coletada = Coleta.objects.filter(data__range=(start_date, today)).annotate(month=ExtractMonth('data')).values('month').annotate(quantidade=Sum('quantidade'))
  return render(request, 'relatorio_coleta.html', {
    'numero_coletas': numero_coletas,
    'maior_coleta': maior_coleta,
    'menor_coleta': menor_coleta,
    'quantidade_coletada': quantidade_coletada
  })

def coleta_list(request):
  coletas = Coleta.objects.all()
  return render(request, 'coletas_list.html', {'coletas': coletas})


def coleta_detail(request, pk):
  coleta = get_object_or_404(Coleta, pk=pk)
  return render(request, 'coleta_detail.html', {'coleta': coleta})

def coleta_delete(request, pk):
  coleta = get_object_or_404(Coleta, pk=pk)
  if request.method == 'POST':
    coleta.delete()
    return redirect('coletas')
  return render(request, 'coleta_confirm_delete.html', {'coleta': coleta})

def coleta_create(request):
  criacoes = Criacao.objects.all()
  if request.method == 'POST':
    form = ColetaForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('coletas')
  else:
    form = ColetaForm()
  return render(request, 'coleta_form.html', {'form': form, 'criacoes': criacoes, 'is_create': True})

def coleta_update(request, pk):
  criacoes = Criacao.objects.all()
  coleta = get_object_or_404(Coleta, pk=pk)
  if request.method == 'POST':
    form = ColetaForm(request.POST, instance=coleta)
    if form.is_valid():
      form.save()
      return redirect('coletas')
  else:
    form = ColetaForm(instance=coleta)
  return render(request, 'coleta_form.html', {'form': form, 'criacoes': criacoes, 'is_create': False, 'pk': pk})


def redirecionar_para_relatorio(request):
  return redirect('relatorio_coleta')
