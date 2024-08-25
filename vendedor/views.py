from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from .models import Vendedor
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import VendedorForm
from django.db import IntegrityError, OperationalError

class cadastrar_vendedor(CreateView):
    model = Vendedor
    form_class = VendedorForm
    template_name = 'vendedor/vendedor_form.html'
    success_url = reverse_lazy('listar_vendedor')

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'vendedor': False})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect(self.success_url)
            except IntegrityError:
                return render(request, self.template_name, {'form': form, 'erro': "Erro de integridade: Dados inválidos."})
            except OperationalError:
                return render(request, self.template_name, {'form': form, 'erro': "Erro operacional: Problema com o banco de dados."})
            except Exception as e:
                return render(request, self.template_name, {'form': form, 'erro': f"Erro inesperado: {e}"})
        else:
            return render(request, self.template_name, {'form': form})

class listar_vendedor(ListView):
    model = Vendedor
    template_name = 'vendedor/vendedor_list.html'

class editar_vendedor(UpdateView):
    model = Vendedor
    form_class = VendedorForm
    template_name = 'vendedor/vendedor_form.html'
    success_url = reverse_lazy('listar_vendedor')

    def get(self, request, *args, **kwargs):
        id = kwargs.get('pk', None)
        vendedor = Vendedor.objects.get(id=id)
        form = self.form_class(instance=vendedor)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        id = kwargs.get('pk', None)
        vendedor = Vendedor.objects.get(id=id)
        form = self.form_class(request.POST, instance=vendedor)
        if form.is_valid():
            try:
                form.save()
                return redirect(self.success_url)
            except IntegrityError:
                return render(request, self.template_name, {'form': form, 'erro': "Erro de integridade: Dados inválidos."})
            except OperationalError:
                return render(request, self.template_name, {'form': form, 'erro': "Erro operacional: Problema com o banco de dados."})
            except Exception as e:
                return render(request, self.template_name, {'form': form, 'erro': f"Erro inesperado: {e}"})
        else:
            return render(request, self.template_name, {'form': form})

class deletar_vendedor(DeleteView):
    model = Vendedor
    template_name = 'vendedor/confirmar_apagar_vendedor.html'
    success_url = reverse_lazy('listar_vendedor')

    def get(self, request, *args, **kwargs):
        try:
            id = kwargs.get('pk', None)
            vendedor = Vendedor.objects.get(id=id)
        except Vendedor.DoesNotExist:
            return HttpResponseNotFound('Vendedor não encontrado.')
        except OperationalError:
            return HttpResponse("Erro operacional: Problema com o banco de dados.", status=500)
        except Exception as e:
            return HttpResponse(f"Erro inesperado: {e}", status=500)
        return render(request, self.template_name, {"vendedor": vendedor})

    def delete(self, request, *args, **kwargs):
        id = kwargs.get('pk', None)
        if id is None:
            return HttpResponseNotFound('Vendedor não encontrado.')
        try:
            vendedor = Vendedor.objects.get(id=id)
            vendedor.delete()
            return JsonResponse({'message': 'Vendedor excluído com sucesso.'}, status=200)
        except Vendedor.DoesNotExist:
            return HttpResponseNotFound('Vendedor não encontrado.')
        except Exception as e:
            return JsonResponse({'message': 'Erro ao excluir vendedor.', 'error': str(e)}, status=500)
