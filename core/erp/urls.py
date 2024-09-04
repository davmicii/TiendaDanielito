from django.urls import path

from app.core.erp.templates.dashboard.views import DashboardView
from app.core.erp.views.categorias.views import CategoriaListView, CategoriaCreateView, CategoriaUpdateView, CategoriaDeleteView
from app.core.erp.views.clientes.views import ClienteCreateView
from app.core.erp.views.detalle_producto.views import DetalleProductoListView
from app.core.erp.views.empresas.views import EmpresaListView, EmpresaCreateView, EmpresaUpdateView, EmpresaDeleteView
from app.core.erp.views.inventario.views import InventarioCreateView
from app.core.erp.views.pagos.views import ListPagoView, CrearPagoView
from app.core.erp.views.productos.views import ProductoListView, ProductoCreateView, ProductoUpdateView, ProductoDeleteView
from app.core.erp.views.proveedores.views import ProveedorListView, ProveedorCreateView, ProveedorDeleteView
from app.core.erp.views.subcategorias.views import SubCategoriaListView, SubCategoriaCreateView, SubCategoriaDeleteView, SubCategoriaUpdateView
from app.core.erp.views.todos_productos.views import TodoProductosListView
from app.core.erp.views.ventas.views import CrearVentaView, ListVentaView, VentaInvocarPDF

app_name = 'erp'

urlpatterns = [
    # Dashboard
    path('dashboard/', DashboardView.as_view(), name='dashboard'),


    # Clientes
    path('clientes/create/', ClienteCreateView.as_view(), name='cliente-create'),

    # Categorias
    path('categorias/', CategoriaListView.as_view(), name='categoria_list'),
    path('categorias/create', CategoriaCreateView.as_view(), name='categoria_create'),
    path('categorias/update/<int:pk>/', CategoriaUpdateView.as_view(), name='categoria_update'),
    path('categorias/delete/<int:pk>/', CategoriaDeleteView.as_view(), name='categoria_delete'),

    # SubCategorias
    path('subcategorias/<str:category_name>/', SubCategoriaListView.as_view(), name='subcategoria_list'),
    path('subcategorias/create/<int:category_id>/<str:category_name>/', SubCategoriaCreateView.as_view(), name='subcategoria_create'),
    path('subcategorias/update/<str:category_name>/<str:subcategory_name>/<int:category_id>/<int:pk>/', SubCategoriaUpdateView.as_view(), name='subcategoria_update'),
    path('subcategorias/delete/<str:category_name>/<str:subcategory_name>/<int:category_id>/<int:pk>/', SubCategoriaDeleteView.as_view(), name='subcategoria_delete'),


    #Empresas
    path('empresas/', EmpresaListView.as_view(), name='empresa_list'),
    path('empresas/create/', EmpresaCreateView.as_view(), name='empresa_create'),
    path('empresas/update/<int:pk>/', EmpresaUpdateView.as_view(), name='empresa_update'),
    path('empresas/delete/<int:pk>/', EmpresaDeleteView.as_view(), name='empresa_delete'),


    # Productos
    path('productos/<str:subcategory_name>/', ProductoListView.as_view(), name='producto_list'),
    path('productos/create/<int:subcategory_id>/<str:subcategory_name>/', ProductoCreateView.as_view(), name='producto_create'),
    path('productos/update/<str:subcategory_name>/<str:product_name>/<int:subcategory_id>/<int:pk>/', ProductoUpdateView.as_view(), name='producto_update'),
    path('productos/delete/<str:subcategory_name>/<str:product_name>/<int:subcategory_id>/<int:pk>/', ProductoDeleteView.as_view(), name='producto_delete'),


    # Detalle de Producto
    path('detalle_producto/<str:product_name>/<int:product_id>/', DetalleProductoListView.as_view(), name='detalle_producto'),


    # Inventario
    path('agregar_inventario/', InventarioCreateView.as_view(), name='agregar_inventario'),


    # Todos los productos
    path('todos_los_productos/', TodoProductosListView.as_view(), name='todos_productos'),


    # Proveedores
    path('proveedores/', ProveedorListView.as_view(), name='proveedor_list'),
    path('proveedor/create/', ProveedorCreateView.as_view(), name='proveedor_create'),
    path('proveedor/delete/<int:pk>/', ProveedorDeleteView.as_view(), name='proveedor_delete'),


    # Ventas
    path('ventas/list/', ListVentaView.as_view(), name='list_venta'),
    path('ventas/create/', CrearVentaView.as_view(), name='crear_venta'),
    path('ventas/invoice/pdf/<int:pk>/', VentaInvocarPDF.as_view(), name='invoice_pdf_venta'),

    # Pagos
    path('pagos/list/', ListPagoView.as_view(), name='list_pago'),
    path('pagos/create/', CrearPagoView.as_view(), name='create_pago'),
]