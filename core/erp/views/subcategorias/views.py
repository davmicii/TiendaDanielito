from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.db import connection
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, DeleteView, UpdateView

from core.erp.forms import SubCategoriaForm
from core.erp.models import SubCategoria, Categoria
from core.erp.mixins import MultiPermissionRequiredMixin


class SubCategoriaListView(MultiPermissionRequiredMixin, ListView):
    model = SubCategoria
    template_name = 'subcategorias/list.html'
    context_object_name = 'subcategorias'
    permissions = ['erp.view_subcategoria']

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        category_name = self.kwargs.get('category_name')
        with connection.cursor() as cursor:
            cursor.callproc('sp_list_subcategorias_by_category_name', [category_name])
            results = cursor.fetchall()

        queryset = [SubCategoria(id=row[0], categoria_id=row[1], nombre=row[2], imagen_subcategoria=row[3]) for row in
                    results]
        return queryset

    def get_category_id_by_name(self, category_name):
        try:
            categoria = Categoria.objects.get(nombre=category_name)
            return categoria.id
        except Categoria.DoesNotExist:
            return None  # O maneja el caso si no se encuentra la categoría

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_name'] = self.kwargs.get('category_name')  # Pasamos category_name al contexto
        # Buscar el ID de la categoría basado en el nombre
        category_id = self.get_category_id_by_name(context['category_name'])
        context['category_id'] = category_id  # Pasamos category_id al contexto
        # Para las opciones
        context['page'] = 'Subcategorías'
        context['title'] = 'Tienda Danielito'
        context['nuevo'] = 'SubCategorías'
        context['entity'] = 'SubCategorías'
        context['action'] = 'searchdata'
        return context


class SubCategoriaCreateView(MultiPermissionRequiredMixin, CreateView):
    model = SubCategoria
    form_class = SubCategoriaForm
    template_name = 'subcategorias/create.html'
    permissions = ['erp.add_subcategoria', 'erp.change_subcategoria', 'erp.delete_subcategoria']

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        # Obtener los parámetros category_id y category_name de la URL
        category_id = self.kwargs['category_id']
        category_name = self.kwargs['category_name']
        # Devolver la URL de la lista de subcategorías con el parámetro category_name
        return reverse_lazy('erp:subcategoria_list', kwargs={'category_name': category_name})

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            category_id = kwargs.get('category_id')
            category_name = kwargs.get('category_name')
            action = request.POST.get('action')

            if action == 'add':
                imagen_subcategoria = request.FILES.get('imagen_subcategoria')
                if imagen_subcategoria:
                    nombre_imagen = imagen_subcategoria.name
                    ruta_guardado = f'imgSubCategoria/{now().year}/{now().month}/{now().day}/{nombre_imagen}'
                    ruta_completa = default_storage.save(ruta_guardado, imagen_subcategoria)

                    with connection.cursor() as cursor:
                        cursor.execute("CALL sp_create_subcategoria(%s, %s, %s)", [
                            request.POST['nombre'],
                            ruta_completa,
                            category_id,
                        ])
                else:
                    with connection.cursor() as cursor:
                        cursor.execute("CALL sp_create_subcategoria(%s, NULL, %s)", [
                            request.POST['nombre'],
                            category_id,
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
        context['category_id'] = self.kwargs.get('category_id')
        context['category_name'] = self.kwargs.get('category_name')
        context['action'] = 'add'
        context['page'] = 'Subcategorías'
        context['title'] = 'Tienda Danielito'
        context['nuevo'] = 'Nueva Subcategoría'
        context['entity'] = 'Subcategorías'
        context['list_url'] = self.get_success_url()
        return context


class SubCategoriaUpdateView(MultiPermissionRequiredMixin, UpdateView):
    model = SubCategoria
    form_class = SubCategoriaForm
    template_name = 'subcategorias/create.html'
    success_url = reverse_lazy('erp:subcategoria_list')
    permissions = ['erp.add_subcategoria', 'erp.change_subcategoria', 'erp.delete_subcategoria']

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        category_name = self.kwargs['category_name']
        return reverse_lazy('erp:subcategoria_list', kwargs={'category_name': category_name})

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            subcategory_id = self.kwargs.get('pk')
            category_id = self.kwargs.get('category_id')
            category_name = self.kwargs.get('category_name')
            action = request.POST.get('action')
            if action == 'edit':
                # Procesa la imagen y guarda la ruta en la base de datos
                imagen_subcategoria = request.FILES.get('imagen_subcategoria')
                if imagen_subcategoria:
                    # Construye la ruta de guardado
                    nombre_imagen = imagen_subcategoria.name
                    ruta_guardado = f'imgSubCategoria/{now().year}/{now().month}/{now().day}/{nombre_imagen}'

                    # Guarda la imagen en el sistema de archivos
                    ruta_completa = default_storage.save(ruta_guardado, imagen_subcategoria)

                    # Convierte request.POST a un diccionario mutable
                    datos_modificables = request.POST.copy()

                    # Asigna la ruta de guardado al campo imagen_facultad
                    datos_modificables['imagen_subcategoria'] = ruta_completa

                    with connection.cursor() as cursor:
                        cursor.execute("CALL sp_update_subcategoria(%s, %s, %s, %s)", [
                            subcategory_id,  # El ID del objeto a editar
                            datos_modificables['nombre'],
                            datos_modificables['imagen_subcategoria'],
                            category_id
                        ])
                else:
                    with connection.cursor() as cursor:
                        cursor.execute("CALL sp_update_subcategoria(%s, %s, NULL, %s)", [
                            subcategory_id,  # El ID del objeto a editar
                            request.POST['nombre'],
                            category_id
                            # request.FILES['imagen_categoria'].name if 'imagen_facultad' in request.FILES else None
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
        context['category_id'] = self.kwargs.get('category_id')
        context['category_name'] = self.kwargs.get('category_name')
        context['page'] = 'Subcategorías'
        context['title'] = 'Tienda Danielito'
        context['nuevo'] = 'Editar SubCategoría'
        context['entity'] = 'SubCategorías'
        context['list_url'] = self.get_success_url()
        context['action'] = 'edit'
        return context


class SubCategoriaDeleteView(MultiPermissionRequiredMixin, DeleteView):
    model = SubCategoria
    template_name = 'subcategorias/delete.html'
    permissions = ['erp.add_subcategoria', 'erp.change_subcategoria', 'erp.delete_subcategoria']

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        category_name = self.kwargs['category_name']
        return reverse_lazy('erp:subcategoria_list', kwargs={'category_name': category_name})

    def post(self, request, *args, **kwargs):
        data = {}
        subcategory_id = self.kwargs.get('pk')
        category_id = self.kwargs.get('category_id')
        category_name = self.kwargs.get('category_name')
        try:
            with connection.cursor() as cursor:
                cursor.execute("CALL sp_delete_subcategoria(%s, %s)", [category_id, subcategory_id])
            data['success'] = True
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'Subcategorías'
        context['title'] = 'Tienda Danielito'
        context['nuevo'] = 'Eliminar SubCategoría'
        context['entity'] = 'SubCategorías'
        context['list_url'] = self.get_success_url()
        context['action'] = 'delete'
        return context
