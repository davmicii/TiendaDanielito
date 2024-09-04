from django.contrib.auth.decorators import login_required
from django.db import connection
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView

from app.core.erp.models import Producto


class TodoProductosListView(ListView):
    model = Producto
    template_name = 'todos_productos/list.html'
    context_object_name = 'todos_productos'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        with connection.cursor() as cursor:
            cursor.callproc('sp_list_all_products')
            results = cursor.fetchall()

        queryset = [Producto(id=row[0], nombre=row[1], imagen_producto=row[2], precio=row[3]) for row in
                    results]
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'Mis Productos'
        context['title'] = 'Tienda Danielito'
        context['nuevo'] = 'Productos'
        context['entity'] = 'Productos'
        context['action'] = 'searchdata'
        return context
