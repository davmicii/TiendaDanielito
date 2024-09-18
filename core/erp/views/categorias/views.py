from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.db import connection
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.erp.forms import CategoriaForm
from core.erp.models import Categoria
from core.erp.mixins import MultiPermissionRequiredMixin


# Create your views here.
class CategoriaListView(MultiPermissionRequiredMixin, ListView):
    model = Categoria
    template_name = 'categorias/list.html'
    permissions = ['erp.view_categoria']

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        # Invocar al SP
        with connection.cursor() as cursor:
            cursor.callproc('sp_list_categorias')
            results = cursor.fetchall()

        # Crear instancias de la tb Categoria
        queryset = [Categoria(*row) for row in results]
        return queryset

    def pos(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in self.get_queryset():
                    data.append(i.tojson())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'Categorías'
        context['title'] = 'Tienda Danielito'
        context['nuevo'] = 'Categorías'
        context['entity'] = 'Categorías'
        context['action'] = 'searchdata'
        return context


class CategoriaCreateView(MultiPermissionRequiredMixin, CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'categorias/create.html'
    permissions = ['erp.add_categoria', 'erp.change_categoria', 'erp.delete_categoria']
    success_url = reverse_lazy('erp:categoria_list')
    # url_redirect = success_url

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                # Procesa la imagen y guarda la ruta en la base de datos
                imagen_categoria = request.FILES.get('imagen_categoria')
                if imagen_categoria:
                    # Construye la ruta de guardado
                    nombre_imagen = imagen_categoria.name
                    ruta_guardado = f'imgCategoria/{now().year}/{now().month}/{now().day}/{nombre_imagen}'

                    # Guarda la imagen en el sistema de archivos
                    ruta_completa = default_storage.save(ruta_guardado, imagen_categoria)

                    # Convierte request.POST a un diccionario mutable
                    datos_modificables = request.POST.copy()

                    # Asigna la ruta de guardado al campo imagen_categoria
                    datos_modificables['imagen_categoria'] = ruta_completa

                    # Llama al procedimiento almacenado para guardar los datos
                    with connection.cursor() as cursor:
                        cursor.execute("CALL sp_insert_categoria(%s, %s)", [
                            datos_modificables['nombre'],
                            datos_modificables['imagen_categoria']
                        ])
                else:
                    # Llama al procedimiento almacenado sin la imagen
                    with connection.cursor() as cursor:
                        cursor.execute("CALL sp_insert_categoria(%s, NULL)", [
                            request.POST['nombre'],
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
        context['page'] = 'Categorías'
        context['title'] = 'Tienda Danielito'
        context['nuevo'] = 'Nueva Categoría'
        context['entity'] = 'Categorías'
        context['list_url'] = reverse_lazy('erp:categoria_list')
        context['action'] = 'add'
        return context


class CategoriaUpdateView(MultiPermissionRequiredMixin, UpdateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'categorias/create.html'
    success_url = reverse_lazy('erp:categoria_list')
    permissions = ['erp.add_categoria', 'erp.change_categoria', 'erp.delete_categoria']

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                # Procesa la imagen y guarda la ruta en la base de datos
                imagen_categoria = request.FILES.get('imagen_categoria')
                if imagen_categoria:
                    # Construye la ruta de guardado
                    nombre_imagen = imagen_categoria.name
                    ruta_guardado = f'imgCategoria/{now().year}/{now().month}/{now().day}/{nombre_imagen}'

                    # Guarda la imagen en el sistema de archivos
                    ruta_completa = default_storage.save(ruta_guardado, imagen_categoria)

                    # Convierte request.POST a un diccionario mutable
                    datos_modificables = request.POST.copy()

                    # Asigna la ruta de guardado al campo imagen_facultad
                    datos_modificables['imagen_categoria'] = ruta_completa

                    with connection.cursor() as cursor:
                        cursor.execute("CALL sp_update_categoria(%s, %s, %s)", [
                            self.object.pk,  # El ID del objeto a editar
                            datos_modificables['nombre'],
                            datos_modificables['imagen_categoria']
                        ])
                else:
                    with connection.cursor() as cursor:
                        cursor.execute("CALL sp_update_categoria(%s, %s, NULL)", [
                            self.object.pk,  # El ID del objeto a editar
                            request.POST['nombre'],
                            # request.FILES['imagen_categoria'].name if 'imagen_facultad' in request.FILES else None
                        ])
                data['success'] = True
                data['redirect_url'] = self.success_url
            else:
                data['error'] = 'No ha ingresado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'Categorías'
        context['title'] = 'Tienda Danielito'
        context['nuevo'] = 'Editar Categoría'
        context['entity'] = 'Categorías'
        context['list_url'] = reverse_lazy('erp:categoria_list')
        context['action'] = 'edit'
        return context


class CategoriaDeleteView(MultiPermissionRequiredMixin, DeleteView):
    model = Categoria
    template_name ='categorias/delete.html'
    success_url = reverse_lazy('erp:categoria_list')
    permissions = ['erp.add_categoria', 'erp.change_categoria', 'erp.delete_categoria']

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            with connection.cursor() as cursor:
                cursor.execute("CALL sp_delete_categoria(%s)", [self.object.pk])
            data['success'] = True
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'Categorías'
        context['title'] = 'Tienda Danielito'
        context['nuevo'] = 'Eliminar Categoría'
        context['entity'] = 'Categorías'
        context['list_url'] = reverse_lazy('erp:categoria_list')
        context['action'] = 'delete'
        return context
