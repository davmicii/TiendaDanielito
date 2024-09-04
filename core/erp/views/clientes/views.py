from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView

from app.core.erp.mixins import MultiPermissionRequiredMixin
from app.core.erp.forms import ClienteForm
from app.core.erp.models import Cliente


class ClienteCreateView(MultiPermissionRequiredMixin, CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'clientes/create.html'
    permissions = ['erp.add_cliente']

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST.get('action', '')
            if action == 'add':
                with connection.cursor() as cursor:
                    cursor.execute('CALL sp_insert_cliente(%s, %s, %s, %s, %s, %s)', [
                        request.POST['nombres'],
                        request.POST['apellidos'],
                        request.POST['cedula'],
                        request.POST['fecha_nacimiento'],
                        request.POST['direccion'],
                        request.POST['genero'],
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
        context['page'] = 'Clientes'
        context['title'] = 'Tienda Danielito'
        context['nuevo'] = 'Agregar Cliente'
        context['entity'] = 'Clientes'
        context['list_url'] = reverse_lazy('erp:crear_venta')
        context['action'] = 'add'
        return context
