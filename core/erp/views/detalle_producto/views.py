from django.contrib.auth.decorators import login_required
from django.db import connection
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView

from app.core.erp.models import Producto


class DetalleProductoListView(ListView):
    model = Producto
    template_name = 'detalle_producto/list.html'
    context_object_name = 'detalle_productos'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        product_name = self.kwargs.get('product_name')
        product_id = self.kwargs.get('product_id')
        with connection.cursor() as cursor:
            cursor.callproc('sp_detail_product_by_name_and_id', [product_name, product_id])
            results = cursor.fetchall()

        queryset = [Producto(id=row[0], subcategoria_id=row[1], empresa_id=row[2], nombre=row[3], descripcion=row[4], precio=row[5], imagen_producto=row[6]) for row in
                    results]
        return queryset

    # def get_subcategory_id_by_name(self, subcategory_name):
    #     try:
    #         subcategoria = SubCategoria.objects.get(nombre=subcategory_name)
    #         return subcategoria.id
    #     except SubCategoria.DoesNotExist:
    #         return None  # O maneja el caso si no se encuentra la categoría

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['subcategory_name'] = self.kwargs.get('subcategory_name')  # Pasamos subcategory_name al contexto
        # Buscar el ID de la subcategoría basado en el nombre
        # subcategory_id = self.get_subcategory_id_by_name(context['subcategory_name'])
        # context['subcategory_id'] = subcategory_id  # Pasamos subcategory_id al contexto
        # Para las opciones
        context['page'] = 'Detalle de Producto'
        context['title'] = 'Tienda Danielito'
        context['nuevo'] = 'Detalle de Producto'
        context['entity'] = 'Detalle de Producto'
        context['action'] = 'searchdata'
        return context
