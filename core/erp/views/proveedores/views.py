from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, DeleteView

from core.erp.forms import ProveedorForm
from core.erp.models import Proveedor, Empresa
from core.erp.mixins import MultiPermissionRequiredMixin


class ProveedorListView(MultiPermissionRequiredMixin, ListView):
    model = Proveedor
    template_name = 'proveedores/list.html'
    context_object_name = 'proveedores'
    permissions = ['erp.add_proveedor', 'erp.change_proveedor', 'erp.delete_proveedor', 'erp.view_proveedor']

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        with connection.cursor() as cursor:
            cursor.callproc('sp_list_proveedores')
            results = cursor.fetchall()

        queryset = []
        for row in results:
            empresa = Empresa.objects.get(pk=row[3])  # Obtener la instancia de Empresa

            # Verifica si bool_dias_visita es una cadena o lista
            dias_visita = row[2]
            if isinstance(dias_visita, str):
                # Si es un string, probablemente venga en formato JSON o similar
                dias_visita = dias_visita.strip('{}').replace('"', '').split(', ')
            elif not isinstance(dias_visita, list):
                dias_visita = [dias_visita]  # Convertir en lista si no es

            proveedor = Proveedor(
                id=row[0],
                nombre=row[1],
                bool_dias_visita=dias_visita,
                empresa=empresa,
                telefono=row[4]
            )
            proveedor.bool_dias_visita_formatted = ', '.join(dias_visita)
            queryset.append(proveedor)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Para las opciones
        context['page'] = 'Proveedores'
        context['title'] = 'Tienda Danielito'
        context['nuevo'] = 'Proveedor'
        context['entity'] = 'Proveedores'
        context['action'] = 'searchdata'
        return context


class ProveedorCreateView(MultiPermissionRequiredMixin, CreateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'proveedores/create.html'
    permissions = ['erp.add_proveedor', 'erp.change_proveedor', 'erp.delete_proveedor', 'erp.view_proveedor']

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        bool_dias_visita = form.cleaned_data['bool_dias_visita']
        print("bool_dias_visita:", bool_dias_visita)  # Verifica el formato
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST.get('action', '')
            if action == 'add':
                # Convertir el campo bool_dias_visita a formato de array para PostgreSQL
                bool_dias_visita = request.POST.getlist('bool_dias_visita')
                bool_dias_visita = '{' + ','.join(bool_dias_visita) + '}'

                with connection.cursor() as cursor:
                    cursor.callproc('sp_insert_proveedor', [
                        request.POST['nombre'],
                        bool_dias_visita,
                        request.POST['empresa'],
                        request.POST['telefono'],
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
        context['page'] = 'Proveedores'
        context['title'] = 'Tienda Danielito'
        context['nuevo'] = 'Agregar Proveedor'
        context['entity'] = 'Proveedores'
        context['list_url'] = reverse_lazy('erp:proveedor_list')
        context['action'] = 'add'
        return context


class ProveedorDeleteView(MultiPermissionRequiredMixin, DeleteView):
    model = Proveedor
    template_name ='proveedores/delete.html'
    success_url = reverse_lazy('erp:proveedor_list')
    permissions = ['erp.add_proveedor', 'erp.change_proveedor', 'erp.delete_proveedor', 'erp.view_proveedor']

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            with connection.cursor() as cursor:
                cursor.execute("CALL sp_delete_proveedor(%s)", [self.object.pk])
            data['success'] = True
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Para las opciones
        context['page'] = 'Proveedores'
        context['title'] = 'Tienda Danielito'
        context['list_url'] = reverse_lazy('erp:proveedor_list')
        context['nuevo'] = 'Eliminar Proveedor'
        context['entity'] = 'Proveedores'
        context['action'] = 'delete'
        return context
