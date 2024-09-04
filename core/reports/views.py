from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.db.models.functions import Coalesce
from django.db.models import Sum, DecimalField

from app.core.erp.models import Categoria, Venta
from app.core.reports.forms import ReportForm


class ReportVentaView(TemplateView):
    template_name = 'ventas/report.html'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = []
        try:
            action = request.POST['action']
            if action == 'search_report':
                start_date = request.POST.get('start_date', '')
                end_date = request.POST.get('end_date', '')
                with connection.cursor() as cursor:
                    cursor.execute("SELECT * FROM sp_list_ventas_by_fecha(%s, %s)", [start_date, end_date])
                    rows = cursor.fetchall()
                    columns = [col[0] for col in cursor.description]
                    for row in rows:
                        data.append(dict(zip(columns, row)))
            else:
                data.append({'error': 'Ha ocurrido un error'})
        except Exception as e:
            data = [{'error': str(e)}]
        return JsonResponse({'data': data}, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'Reportes'
        context['title'] = 'Tienda Danielito'
        context['nuevo'] = 'Reportes'
        context['entity'] = 'Reportes'
        context['action'] = 'search_report'
        context['list_url'] = reverse_lazy('report_venta')
        context['form'] = ReportForm()
        return context
