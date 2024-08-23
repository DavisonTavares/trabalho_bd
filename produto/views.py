from django.shortcuts import render
from .models import Produto
from django.views.generic import ListView,CreateView
from django.urls import reverse_lazy

class criar_produto(CreateView):
    model = Produto
    fields = ['nome','id','quantidade','valor','marca','litragem']
