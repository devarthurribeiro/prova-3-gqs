
from django.contrib import admin
from django.urls import path
from app_mel import views
urlpatterns = [
    path('', views.redirecionar_para_relatorio),
    path('relatorio_coleta', views.relatorio_coleta, name='relatorio_coleta'),
    path('coletas/', views.coleta_list, name='coletas'),
    path('coletas/<int:pk>/', views.coleta_detail, name='coleta_detail'),
    path('coletas/<int:pk>/delete/', views.coleta_delete, name='coleta_delete'),
    path('coletas/create/', views.coleta_create, name='coleta_create'),
    path('coletas/<int:pk>/update/', views.coleta_update, name='coleta_update'),

]
