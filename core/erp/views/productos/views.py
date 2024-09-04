from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.db import connection
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from app.core.erp.forms import ProductoForm
from app.core.erp.models import Producto, SubCategoria
from app.core.erp.mixins import MultiPermissionRequiredMixin


class ProductoListView(MultiPermissionRequiredMixin, ListView):
    model = Producto
    template_name = 'productos/list.html'
    context_object_name = 'productos'
    permissions = ['erp.view_producto']

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        subcategory_name = self.kwargs.get('subcategory_name')
        with connection.cursor() as cursor:
            cursor.callproc('sp_list_products_by_subcategory_name', [subcategory_name])
            results = cursor.fetchall()

        queryset = [Producto(id=row[0], subcategoria_id=row[1], empresa_id=row[2], nombre=row[3], descripcion=row[4], precio=row[5], imagen_producto=row[6]) for row in
                    results]
        return queryset

    def get_subcategory_id_by_name(self, subcategory_name):
        try:
            subcategoria = SubCategoria.objects.get(nombre=subcategory_name)
            return subcategoria.id
        except SubCategoria.DoesNotExist:
            return None  # O maneja el caso si no se encuentra la categoría

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subcategory_name'] = self.kwargs.get('subcategory_name')  # Pasamos subcategory_name al contexto
        # Buscar el ID de la subcategoría basado en el nombre
        subcategory_id = self.get_subcategory_id_by_name(context['subcategory_name'])
        context['subcategory_id'] = subcategory_id  # Pasamos subcategory_id al contexto
        # Para las opciones
        context['page'] = 'Productos'
        context['title'] = 'Tienda Danielito'
        context['nuevo'] = 'Producto'
        context['entity'] = 'Productos'
        context['action'] = 'searchdata'
        return context


class ProductoCreateView(MultiPermissionRequiredMixin, CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'productos/create.html'
    permissions = ['erp.add_producto', 'erp.change_producto', 'erp.delete_producto']

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        # Obtener los parámetros subcategory_id y subcategory_name de la URL
        subcategory_id = self.kwargs['subcategory_id']
        subcategory_name = self.kwargs['subcategory_name']
        # Devolver la URL de la lista de productos con el parámetro subcategory_name
        return reverse_lazy('erp:producto_list', kwargs={'subcategory_name': subcategory_name})

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            subcategory_id = kwargs.get('subcategory_id')
            subcategory_name = kwargs.get('subcategory_name')
            action = request.POST.get('action')

            if action == 'add':
                imagen_producto = request.FILES.get('imagen_producto')
                if imagen_producto:
                    nombre_imagen = imagen_producto.name
                    ruta_guardado = f'imgProducto/{now().year}/{now().month}/{now().day}/{nombre_imagen}'
                    ruta_completa = default_storage.save(ruta_guardado, imagen_producto)

                    with connection.cursor() as cursor:
                        cursor.execute("CALL sp_create_producto(%s, %s, %s, %s, %s, %s)", [
                            request.POST['nombre'],
                            request.POST['descripcion'],
                            request.POST['precio'],
                            ruta_completa,
                            subcategory_id,
                            request.POST['empresa'],
                        ])
                else:
                    with connection.cursor() as cursor:
                        cursor.execute("CALL sp_create_producto(%s, %s, %s, %s, %s, NULL)", [
                            request.POST['nombre'],
                            request.POST['descripcion'],
                            request.POST['precio'],
                            subcategory_id,
                            request.POST['empresa'],
                        ])
                data['success'] = True
                data['redirect_url'] = str(self.get_success_url())
            else:
                data['error'] = 'No ha ingresado ninguna opción válida'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subcategory_id'] = self.kwargs.get('subcategory_id')
        context['subcategory_name'] = self.kwargs.get('subcategory_name')
        context['action'] = 'add'
        context['page'] = 'Productos'
        context['title'] = 'Tienda Danielito'
        context['nuevo'] = 'Nuevo Producto'
        context['entity'] = 'Productos'
        context['list_url'] = self.get_success_url()
        return context


class ProductoUpdateView(MultiPermissionRequiredMixin, UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'productos/create.html'
    success_url = reverse_lazy('erp:producto_list')
    permissions = ['erp.add_producto', 'erp.change_producto', 'erp.delete_producto']

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        subcategory_name = self.kwargs['subcategory_name']
        return reverse_lazy('erp:producto_list', kwargs={'subcategory_name': subcategory_name})

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            product_id = self.kwargs.get('pk')
            subcategory_id = self.kwargs.get('subcategory_id')
            subcategory_name = self.kwargs.get('subcategory_name')
            action = request.POST.get('action')
            if action == 'edit':
                # Procesa la imagen y guarda la ruta en la base de datos
                imagen_producto = request.FILES.get('imagen_producto')
                if imagen_producto:
                    # Construye la ruta de guardado
                    nombre_imagen = imagen_producto.name
                    ruta_guardado = f'imgProducto/{now().year}/{now().month}/{now().day}/{nombre_imagen}'

                    # Guarda la imagen en el sistema de archivos
                    ruta_completa = default_storage.save(ruta_guardado, imagen_producto)

                    # Convierte request.POST a un diccionario mutable
                    datos_modificables = request.POST.copy()

                    # Asigna la ruta de guardado al campo imagen_facultad
                    datos_modificables['imagen_producto'] = ruta_completa

                    with connection.cursor() as cursor:
                        cursor.execute("CALL sp_update_producto(%s, %s, %s, %s, %s, %s, %s)", [
                            product_id,  # El ID del objeto a editar
                            datos_modificables['nombre'],
                            datos_modificables['descripcion'],
                            datos_modificables['precio'],
                            datos_modificables['imagen_producto'],
                            subcategory_id,
                            datos_modificables['empresa']
                        ])
                else:
                    with connection.cursor() as cursor:
                        cursor.execute("CALL sp_update_producto(%s, %s, %s, %s, %s, %s, NULL)", [
                            product_id,  # El ID del objeto a editar
                            request.POST['nombre'],
                            request.POST['descripcion'],
                            request.POST['precio'],
                            subcategory_id,
                            request.POST['empresa']
                        ])
                data['success'] = True
                data['redirect_url'] = self.get_success_url()
            else:
                data['error'] = 'No ha ingresado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subcategory_id'] = self.kwargs.get('subcategory_id')
        context['subcategory_name'] = self.kwargs.get('subcategory_name')
        context['page'] = 'Productos'
        context['title'] = 'Tienda Danielito'
        context['nuevo'] = 'Editar Producto'
        context['entity'] = 'Productos'
        context['list_url'] = self.get_success_url()
        context['action'] = 'edit'
        return context


class ProductoDeleteView(MultiPermissionRequiredMixin, DeleteView):
    model = Producto
    template_name = 'productos/delete.html'
    permissions = ['erp.add_producto', 'erp.change_producto', 'erp.delete_producto']

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        subcategory_name = self.kwargs['subcategory_name']
        return reverse_lazy('erp:producto_list', kwargs={'subcategory_name': subcategory_name})

    def post(self, request, *args, **kwargs):
        data = {}
        product_id = self.kwargs.get('pk')
        subcategory_id = self.kwargs.get('subcategory_id')
        subcategory_name = self.kwargs.get('subcategory_name')
        try:
            with connection.cursor() as cursor:
                cursor.execute("CALL sp_delete_producto(%s, %s)", [subcategory_id, product_id])
            data['success'] = True
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'Productos'
        context['title'] = 'Tienda Danielito'
        context['nuevo'] = 'Eliminar Producto'
        context['entity'] = 'Productos'
        context['list_url'] = self.get_success_url()
        context['action'] = 'delete'
        return context