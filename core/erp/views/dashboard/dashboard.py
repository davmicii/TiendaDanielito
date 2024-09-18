from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.db import connection
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView


class DashboardListView(TemplateView):
    template_name = 'dashboard/list.html'    

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_ventas_diarias(self):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM get_ventas_diarias();")
            ventas = cursor.fetchall()
        return ventas

    def get_gastos_diarios(self):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM get_gastos_diarios();")
            gastos = cursor.fetchall()
        return gastos

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'Dashboard'
        context['title'] = 'Tienda Danielito'        
        context['entity'] = 'Dashboard'
        context['action'] = 'searchdata'
        context['rep_ventas'] = reverse_lazy('report_venta')
        context['rep_pagos'] = reverse_lazy('report_pago')
        context['ventas_diarias'] = self.get_ventas_diarias()
        context['gastos_diarios'] = self.get_gastos_diarios()
        return context
