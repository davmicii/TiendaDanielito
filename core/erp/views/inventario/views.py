from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView

from app.core.erp.forms import InventarioForm
from app.core.erp.mixins import MultiPermissionRequiredMixin
from app.core.erp.models import Inventario


class InventarioCreateView(MultiPermissionRequiredMixin, CreateView):
    model = Inventario
    form_class = InventarioForm
    template_name = 'inventario/create.html'
    permissions = ['erp.add_inventario']

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
                    cursor.execute("CALL sp_insert_inventario(%s, %s)", [
                        request.POST['cantidad'],
                        request.POST['producto'],
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
        context['page'] = 'Inventario'
        context['title'] = 'Tienda Danielito'
        context['nuevo'] = 'Agregar Inventario'
        context['entity'] = 'Inventario'
        context['list_url'] = reverse_lazy('erp:categoria_list')
        context['action'] = 'add'
        return context
