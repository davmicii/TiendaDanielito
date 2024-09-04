from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.db import connection
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from app.core.erp.forms import EmpresaForm
from app.core.erp.models import Empresa
from app.core.erp.mixins import MultiPermissionRequiredMixin


class EmpresaListView(MultiPermissionRequiredMixin, ListView):
    model = Empresa
    template_name = 'empresas/list.html'
    permissions = ['erp.add_empresa', 'erp.change_empresa', 'erp.delete_empresa', 'erp.view_empresa']

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        # Invocar al SP
        with connection.cursor() as cursor:
            cursor.callproc('sp_list_empresas')
            results = cursor.fetchall()

        # Crear instancias de la tb Empresa
        queryset = [Empresa(*row) for row in results]
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
        context['page'] = 'Empresas'
        context['title'] = 'Tienda Danielito'
        context['nuevo'] = 'Empresas'
        context['entity'] = 'Empresas'
        context['action'] = 'searchdata'
        return context


class EmpresaCreateView(MultiPermissionRequiredMixin, CreateView):
    model = Empresa
    form_class = EmpresaForm
    template_name = 'empresas/create.html'
    success_url = reverse_lazy('erp:empresa_list')
    permissions = ['erp.add_empresa', 'erp.change_empresa', 'erp.delete_empresa', 'erp.view_empresa']
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
                imagen_empresa = request.FILES.get('imagen_empresa')
                if imagen_empresa:
                    # Construye la ruta de guardado
                    nombre_imagen = imagen_empresa.name
                    ruta_guardado = f'imgEmpresa/{now().year}/{now().month}/{now().day}/{nombre_imagen}'

                    # Guarda la imagen en el sistema de archivos
                    ruta_completa = default_storage.save(ruta_guardado, imagen_empresa)

                    # Convierte request.POST a un diccionario mutable
                    datos_modificables = request.POST.copy()

                    # Asigna la ruta de guardado al campo imagen_empresa
                    datos_modificables['imagen_empresa'] = ruta_completa

                    # Llama al procedimiento almacenado para guardar los datos
                    with connection.cursor() as cursor:
                        cursor.execute("CALL sp_insert_empresa(%s, %s, %s)", [
                            datos_modificables['nombre'],
                            datos_modificables['direccion'],
                            datos_modificables['imagen_empresa']
                        ])
                else:
                    # Llama al procedimiento almacenado sin la imagen
                    with connection.cursor() as cursor:
                        cursor.execute("CALL sp_insert_empresa(%s, %s, NULL)", [
                            request.POST['nombre'],
                            request.POST['direccion'],
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
        context['page'] = 'Empresas'
        context['title'] = 'Tienda Danielito'
        context['nuevo'] = 'Nueva Empresa'
        context['entity'] = 'Empresas'
        context['list_url'] = reverse_lazy('erp:empresa_list')
        context['action'] = 'add'
        return context


class EmpresaUpdateView(MultiPermissionRequiredMixin, UpdateView):
    model = Empresa
    form_class = EmpresaForm
    template_name = 'empresas/create.html'
    success_url = reverse_lazy('erp:empresa_list')
    permissions = ['erp.add_empresa', 'erp.change_empresa', 'erp.delete_empresa', 'erp.view_empresa']

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
                imagen_empresa = request.FILES.get('imagen_empresa')
                if imagen_empresa:
                    # Construye la ruta de guardado
                    nombre_imagen = imagen_empresa.name
                    ruta_guardado = f'imgEmpresa/{now().year}/{now().month}/{now().day}/{nombre_imagen}'

                    # Guarda la imagen en el sistema de archivos
                    ruta_completa = default_storage.save(ruta_guardado, imagen_empresa)

                    # Convierte request.POST a un diccionario mutable
                    datos_modificables = request.POST.copy()

                    # Asigna la ruta de guardado al campo imagen_empresa
                    datos_modificables['imagen_empresa'] = ruta_completa

                    with connection.cursor() as cursor:
                        cursor.execute("CALL sp_update_empresa(%s, %s, %s, %s)", [
                            self.object.pk,  # El ID del objeto a editar
                            datos_modificables['nombre'],
                            datos_modificables['direccion'],
                            datos_modificables['imagen_empresa']
                        ])
                else:
                    with connection.cursor() as cursor:
                        cursor.execute("CALL sp_update_empresa(%s, %s, %s, NULL)", [
                            self.object.pk,  # El ID del objeto a editar
                            request.POST['nombre'],
                            request.POST['direccion'],
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
        context['page'] = 'Empresas'
        context['title'] = 'Tienda Danielito'
        context['nuevo'] = 'Editar Empresa'
        context['entity'] = 'Empresas'
        context['list_url'] = reverse_lazy('erp:empresa_list')
        context['action'] = 'edit'
        return context


class EmpresaDeleteView(MultiPermissionRequiredMixin, DeleteView):
    model = Empresa
    template_name ='empresas/delete.html'
    success_url = reverse_lazy('erp:empresa_list')
    permissions = ['erp.add_empresa', 'erp.change_empresa', 'erp.delete_empresa', 'erp.view_empresa']

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            with connection.cursor() as cursor:
                cursor.execute("CALL sp_delete_empresa(%s)", [self.object.pk])
            data['success'] = True
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'Empresas'
        context['title'] = 'Tienda Danielito'
        context['nuevo'] = 'Eliminar Empresa'
        context['entity'] = 'Empresas'
        context['list_url'] = reverse_lazy('erp:empresa_list')
        context['action'] = 'delete'
        return context
