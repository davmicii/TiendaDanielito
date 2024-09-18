import json

from django.contrib.auth.decorators import login_required
from django.db import connection, transaction
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView

from core.erp.forms import PagoForm
from core.erp.mixins import MultiPermissionRequiredMixin
from core.erp.models import Pago


class ListPagoView(MultiPermissionRequiredMixin, ListView):
    model = Pago
    template_name = 'pagos/list.html'
    permission = ['erp.add_pago', 'erp.change_pago', 'erp.delete_pago', 'erp.view_pago']

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        # Invocar al SP para listar pagos
        with connection.cursor() as cursor:
            cursor.callproc('sp_list_pagos')
            results = cursor.fetchall()

        # Convertir los resultados a diccionarios
        queryset = [{
            'pago_id': row[0],
            'fecha_pago': row[1],
            'total': row[2],
            'empresa_nombre': row[3]
        } for row in results]
        return queryset

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST.get('action', '')
            if action == 'searchdata':
                data = []
                for i in self.get_queryset():
                    data.append(i)
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'Pagos'
        context['title'] = 'Tienda Danielito'
        context['nuevo'] = 'Listado de Pagos'
        context['entity'] = 'Pagos'
        context['create_url'] = reverse_lazy('erp:create_pago')
        context['list_url'] = reverse_lazy('erp:list_pago')
        return context


class CrearPagoView(MultiPermissionRequiredMixin, CreateView):
    model = Pago
    form_class = PagoForm
    template_name = 'pagos/create.html'
    success_url = reverse_lazy('erp:dashboard')
    url_redirect = success_url
    permission = ['erp.add_pago', 'erp.change_pago', 'erp.delete_pago', 'erp.view_pago']

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                with connection.cursor() as cursor:
                    cursor.execute("CALL sp_insert_pago(%s, %s, %s)", [
                        request.POST['fecha_pago'],
                        request.POST['total'],
                        request.POST['empresa'],
                    ])
                data['success'] = True
                data['redirect_url'] = str(self.success_url)
            else:
                data['error'] = 'No ha ingresado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'Pagos'
        context['title'] = 'Tienda Danielito'
        context['nuevo'] = 'Registrar Pago'
        context['entity'] = 'Pagos'
        context['list_url'] = reverse_lazy('erp:list_pago')
        context['action'] = 'add'
        return context
