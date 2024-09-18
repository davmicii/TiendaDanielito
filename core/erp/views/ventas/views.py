import json
import os

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db import connection, transaction
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, ListView, View
from xhtml2pdf import pisa

from core.erp.forms import VentaForm
from core.erp.models import Venta
from core.erp.mixins import MultiPermissionRequiredMixin


class ListVentaView(MultiPermissionRequiredMixin, ListView):
    model = Venta
    template_name = 'ventas/list.html'
    permissions = ['erp.add_venta', 'erp.change_venta', 'erp.delete_venta', 'erp.view_venta']

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        # Invocar al SP para listar ventas
        with connection.cursor() as cursor:
            cursor.callproc('sp_list_ventas')
            results = cursor.fetchall()

        # Convertir los resultados a diccionarios
        queryset = [{
            'venta_id': row[0],
            'fecha_venta': row[1],
            'subtotal': row[2],
            'iva': row[3],
            'total': row[4],
            'cliente_nombre': row[5]
        } for row in results]
        return queryset

    def get_detalle_queryset(self, venta_id):
        # Invocar al SP para listar detalles de una venta específica
        with connection.cursor() as cursor:
            cursor.callproc('sp_list_detalle_venta', [venta_id])
            results = cursor.fetchall()

        # Convertir los resultados a diccionarios
        queryset = [{
            'producto_nombre': row[0],
            'cantidad': row[1],
            'precio': row[2],
            'subtotal': row[3]
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
            elif action == 'search_details_prod':
                venta_id = request.POST.get('venta_id')
                data = []
                for i in self.get_detalle_queryset(venta_id):
                    data.append(i)
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'Ventas'
        context['title'] = 'Tienda Danielito'
        context['nuevo'] = 'Listado de Ventas'
        context['entity'] = 'Ventas'
        context['create_url'] = reverse_lazy('erp:crear_venta')
        context['list_url'] = reverse_lazy('erp:list_venta')
        return context


class CrearVentaView(MultiPermissionRequiredMixin, CreateView):
    model = Venta
    form_class = VentaForm
    template_name = 'ventas/create.html'
    success_url = reverse_lazy('erp:dashboard')
    url_redirect = success_url
    permissions = ['erp.add_venta', 'erp.change_venta', 'erp.delete_venta', 'erp.view_venta']

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST.get('action', '')
            term = request.POST.get('term', '')
            if action == 'search_products':
                data = []
                with connection.cursor() as cursor:
                    cursor.callproc('sp_search_products', [term])
                    results = cursor.fetchall()
                    for row in results:
                        item = {
                            'id': row[0],
                            'subcategoria': row[1],
                            'nombre': row[2],
                            'precio': row[3],
                            'value': row[2],
                        }
                        data.append(item)
            elif action == 'add':
                with transaction.atomic():
                    vents = json.loads(request.POST['vents'])
                    with connection.cursor() as cursor:
                        cursor.callproc('sp_insert_venta', [
                            vents['date_joined'],
                            float(vents['subtotal']),
                            float(vents['iva']),
                            float(vents['total']),
                            int(vents['cli'])
                        ])
                        new_venta_id = cursor.fetchone()[0]
                        for i in vents['products']:
                            cursor.execute("CALL sp_insert_detalle_venta(%s, %s, %s, %s, %s)", [
                                new_venta_id,
                                int(i['id']),
                                int(i['cant']),
                                float(i['precio']),
                                float(i['subtotal'])
                            ])
                        data = {'id': new_venta_id}
                data['success'] = True
            else:
                data['error'] = 'No ha ingresado ninguna opción'
        except Exception as e:
            data = {'error': str(e)}
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'Ventas'
        context['title'] = 'Tienda Danielito'
        context['nuevo'] = 'Registrar Venta'
        context['entity'] = 'Ventas'
        context['list_url'] = reverse_lazy('erp:list_venta')
        context['action'] = 'add'
        return context


class VentaInvocarPDF(MultiPermissionRequiredMixin, View):
    permissions = ['erp.add_venta', 'erp.change_venta', 'erp.delete_venta', 'erp.view_venta']
    def link_callback(self, uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those
        resources
        """
        # use short variable names
        sUrl = settings.STATIC_URL  # Typically /static/
        sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL  # Typically /static/media/
        mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

        # convert URIs to absolute system paths
        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri  # handle absolute uri (ie: http://some.tld/foo.png)

        # make sure that file exists
        if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
        return path

    def get_queryset(self, venta_id):
        # Invocar al SP para listar ventas
        with connection.cursor() as cursor:
            cursor.callproc('sp_list_ventas_by_id', [venta_id])
            results = cursor.fetchall()

            # Convertir los resultados a diccionarios
            venta_data = {
                'venta_id': results[0][0],
                'fecha_venta': results[0][1],
                'subtotal': results[0][2],
                'iva': results[0][3],
                'total': results[0][4],
                'cliente_nombre': results[0][5],
                'cedula': results[0][6],
                'detalles': []
            }

            for row in results:
                detalle = {
                    'producto_nombre': row[7],
                    'cantidad': row[8],
                    'precio': row[9],
                    'subtotal': row[10]
                }
                venta_data['detalles'].append(detalle)

            return venta_data

    def get(self, request, *args, **kwargs):
        try:
            venta_id = self.kwargs['pk']
            venta_data = self.get_queryset(venta_id)
            if not venta_data:
                return HttpResponseRedirect(reverse_lazy('erp:list_venta'))

            template = get_template('ventas/invoice.html')
            context = {
                'venta': venta_data,
                'comp': {'name': 'Tienda Danielito', 'ruc': '1350789853001', 'address': 'El Empalme - Parroquia El '
                                                                                       'Rosario'},
                'icon': '{}{}'.format(settings.MEDIA_URL, 'logo.svg')
            }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            pisaStatus = pisa.CreatePDF(
                html, dest=response,
                link_callback=self.link_callback
            )
            return response
        except Exception as e:
            print(e)
        return HttpResponseRedirect(reverse_lazy('erp:list_venta'))
