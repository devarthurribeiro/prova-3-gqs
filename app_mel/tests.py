from django.test import TestCase, Client
from django.urls import reverse
from datetime import date, timedelta, timezone, datetime
from django.utils import timezone
from app_mel.forms import ColetaForm
from app_mel.models import Criacao, Coleta
from django.template.defaultfilters import floatformat

class CriacaoModelTest(TestCase):
  def setUp(self):
    self.criacao = Criacao.objects.create(
      id=1,
      raca="Apis mellifera",
      data_entrada=date.today(),
    )

  def test_max_length_raca(self):
    self.assertEqual(self.criacao._meta.get_field('raca').max_length, 120)

  def test_required_fields(self):
    self.assertTrue(self.criacao._meta.get_field('raca').blank, False)
    self.assertTrue(self.criacao._meta.get_field('data_entrada').blank, False)

  def test_verbose_name(self):
    self.assertEqual(self.criacao._meta.get_field('raca').verbose_name, "raca")
    self.assertEqual(self.criacao._meta.get_field('data_entrada').verbose_name, "data entrada")

class CriacaoModelTest(TestCase):
  def setUp(self):
    self.criacao = Criacao.objects.create(
      id=1,
      raca="Apis mellifera",
      data_entrada=date.today(),
    )

  def test_max_length_raca(self):
    self.assertEqual(self.criacao._meta.get_field('raca').max_length, 120)

  def test_required_fields(self):
    self.assertFalse(self.criacao._meta.get_field('raca').blank)
    self.assertFalse(self.criacao._meta.get_field('data_entrada').blank)

  def test_verbose_name(self):
    self.assertEqual(self.criacao._meta.get_field('raca').verbose_name, "raca")
    self.assertEqual(self.criacao._meta.get_field('data_entrada').verbose_name, "data entrada")

class ColetaModelTest(TestCase):
  def setUp(self):
    self.criacao = Criacao.objects.create(
      id=1,
      raca="Apis mellifera",
      data_entrada=date.today(),
    )
    self.coleta = Coleta.objects.create(
      id=1,
      criacao=self.criacao,
      data=date.today(),
      quantidade=10.5
    )
    self.coleta2 = Coleta.objects.create(
      id=2,
      criacao=self.criacao,
      data=date.today() - timedelta(days=1),
      quantidade=12.3
    )

  def test_required_fields(self):
    self.assertFalse(self.coleta._meta.get_field('criacao').blank)
    self.assertFalse(self.coleta._meta.get_field('data').blank)
    self.assertFalse(self.coleta._meta.get_field('quantidade').blank)

  def test_ordering(self):
    coletas = Coleta.objects.all()
    self.assertTrue(coletas[0].data >= coletas[1].data)


class ColetaListViewTest(TestCase):
  @classmethod
  def setUpTestData(cls):
    criacao = Criacao.objects.create(
      id=1,
      raca="Apis mellifera",
      data_entrada=date.today(),
    )
    number_of_coletas = 5
    for coleta_id in range(number_of_coletas):
      Coleta.objects.create(
        id=coleta_id,
        criacao=criacao,
        data=date.today(),
        quantidade=10.5,
      )

  def setUp(self):
    self.client = Client()

  def test_url_exists_at_desired_location(self):
    response = self.client.get('/coletas/')
    self.assertEqual(response.status_code, 200)

  def test_url_accessible_by_name(self):
    response = self.client.get(reverse('coletas'))
    self.assertEqual(response.status_code, 200)

  def test_uses_correct_template(self):
    response = self.client.get(reverse('coletas'))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'coletas_list.html')

  def test_list_all_coletas(self):
    response = self.client.get(reverse('coletas'))
    self.assertEqual(response.status_code, 200)
    self.assertTrue(len(response.context['coletas']) == 5)

class ColetaDetailViewTest(TestCase):
  @classmethod
  def setUpTestData(cls):
    criacao = Criacao.objects.create(raca="Apis mellifera", data_entrada=date.today())
    Coleta.objects.create(criacao=criacao, data=date.today(), quantidade=0.500)

  def setUp(self):
    self.client = Client()
    self.first_coleta = Coleta.objects.first()

  def test_url_exists_at_desired_location(self):
    response = self.client.get(f'/coletas/{self.first_coleta.id}/')
    self.assertEqual(response.status_code, 200)

  def test_url_accessible_by_name(self):
    response = self.client.get(reverse('coleta_detail', args=[self.first_coleta.id]))
    self.assertEqual(response.status_code, 200)

  def test_correct_template_used(self):
    response = self.client.get(reverse('coleta_detail', args=[self.first_coleta.id]))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'coleta_detail.html')

  def test_object_details(self):
    response = self.client.get(reverse('coleta_detail', args=[self.first_coleta.id]))
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.context['coleta'], self.first_coleta)

class ColetaDeleteViewTest(TestCase):
  @classmethod
  def setUpTestData(cls):
    criacao = Criacao.objects.create(raca="Apis mellifera", data_entrada=date.today())
    Coleta.objects.create(criacao=criacao, data=date.today(), quantidade=0.500)

  def setUp(self):
    self.client = Client()
    self.first_coleta = Coleta.objects.first()

  def test_url_exists_at_desired_location(self):
    response = self.client.get(f'/coletas/{self.first_coleta.id}/delete/')
    self.assertEqual(response.status_code, 200)

  def test_url_accessible_by_name(self):
    response = self.client.get(reverse('coleta_delete', args=[self.first_coleta.id]))
    self.assertEqual(response.status_code, 200)

  def test_correct_template_used(self):
    response = self.client.get(reverse('coleta_delete', args=[self.first_coleta.id]))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'coleta_confirm_delete.html')

  def test_deletes_coleta(self):
    response = self.client.post(reverse('coleta_delete', args=[self.first_coleta.id]))
    self.assertRedirects(response, reverse('coletas'))
    self.assertFalse(Coleta.objects.filter(id=self.first_coleta.id).exists())

class ColetaFormTest(TestCase):
  def setUp(self):
    self.criacao = Criacao.objects.create(raca='Apis mellifera', data_entrada=timezone.now().date())

  def test_coleta_form_valid_data(self):
    form = ColetaForm(data={'criacao': self.criacao, 'data': timezone.now().date(), 'quantidade': 1.5})
    self.assertTrue(form.is_valid())

  def test_coleta_form_blank_data(self):
    form = ColetaForm(data={})
    self.assertFalse(form.is_valid())
    self.assertEqual(form.errors['criacao'], ['Este campo é obrigatório.'])
    self.assertEqual(form.errors['data'], ['Este campo é obrigatório.'])
    self.assertEqual(form.errors['quantidade'], ['Este campo é obrigatório.'])

  def test_coleta_form_future_date(self):
    form = ColetaForm(data={'criacao': self.criacao, 'data': timezone.now().date() + timezone.timedelta(days=1), 'quantidade': 1.5})
    self.assertFalse(form.is_valid())
    self.assertEqual(form.errors['data'], ['A data não pode ser no futuro.'])

  def test_coleta_form_duplicate_date(self):
    Coleta.objects.create(criacao=self.criacao, data=timezone.now().date(), quantidade=1.0)
    form = ColetaForm(data={'criacao': self.criacao, 'data': timezone.now().date(), 'quantidade': 1.5})
    self.assertFalse(form.is_valid())
    self.assertEqual(form.errors['data'], ['Já existe uma coleta registrada nesta data.'])

class EditarColetaViewTest(TestCase):
  def setUp(self):
    self.criacao = Criacao.objects.create(raca='Apis mellifera', data_entrada='2022-01-01')
    self.coleta = Coleta.objects.create(criacao=self.criacao, data='2022-02-01', quantidade=1.5)
    self.url = reverse('coleta_update', args=[self.coleta.pk])
    self.data = {
      'criacao': self.criacao.pk,
      'data':  date(2023, 3, 1),
      'quantidade': 2.0
    }

  def test_url_exists_at_desired_location(self):
    response = self.client.get(self.url)
    self.assertEqual(response.status_code, 200)

  def test_uses_correct_template(self):
    response = self.client.get(self.url)
    self.assertTemplateUsed(response, 'coleta_form.html')

  def test_edita_coleta_corretamente(self):
    response = self.client.post(self.url, data=self.data)
    self.assertEqual(response.status_code, 302)

    self.coleta.refresh_from_db()
    self.assertEqual(self.coleta.data, self.data['data'])
    self.assertEqual(self.coleta.quantidade, self.data['quantidade'])

class RelatorioColetaViewTest(TestCase):
  def setUp(self):
    self.url = reverse('relatorio_coleta')

  def test_url_exists_at_desired_location(self):
    response = self.client.get(self.url)
    self.assertEqual(response.status_code, 200)

  def test_uses_correct_template(self):
    response = self.client.get(self.url)
    self.assertTemplateUsed(response, 'relatorio_coleta.html')

  def test_exibe_relatorio_corretamente(self):
    current_year_string = str(datetime.now().year)
    criacao = Criacao.objects.create(raca='Apis mellifera', data_entrada='2022-01-01')
    coleta1 = Coleta.objects.create(data=f'{current_year_string}-01-01', quantidade=10.5, criacao=criacao)
    coleta2 = Coleta.objects.create(data=f'{current_year_string}-02-01', quantidade=15.2, criacao=criacao)
    coleta3 = Coleta.objects.create(data=f'{current_year_string}-03-01', quantidade=8.7,  criacao=criacao)

    response = self.client.get(self.url)
    self.assertEqual(response.status_code, 200)

    self.assertContains(response, 'Relatório de Coleta')
    self.assertContains(response, f'{floatformat(coleta1.quantidade, 3)}kg')
    self.assertContains(response, f'{floatformat(coleta2.quantidade, 3)}kg')
    self.assertContains(response, f'{floatformat(coleta3.quantidade, 3)}kg')
