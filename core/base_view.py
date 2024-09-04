from django.views.generic import TemplateView


class BaseView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Tienda Danielito'
        context['clientes'] = 'Clientes'
        context['categorias'] = 'Categorías'
        context['empresas'] = 'Empresas'
        context['productos'] = 'Productos'
        context['precios'] = 'Precios'
        context['inventario'] = 'Inventario'
        context['proveedores'] = 'Proveedores'
        context['contactos'] = 'Contactos'
        context['ubicaciones'] = 'Ubicaciones'
        context['facturas'] = 'Facturas'
        context['ventas'] = 'Ventas'
        return context
