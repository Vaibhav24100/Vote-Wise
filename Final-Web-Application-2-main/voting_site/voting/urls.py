from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_a_form, name='create_a_form'),
    path('vote/', views.vote_on_a_form, name='vote_on_a_form'),
    path('result/', views.result, name='result'),
]
