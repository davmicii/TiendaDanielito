# erp/navigation.py

NAVIGATION_OPTIONS = {
    'Administrador': [
        {'name': 'Categorías', 'url': 'erp:categoria_list'},
        {'name': 'Productos', 'url': 'erp:todos_productos'},
        {'name': 'Ventas', 'url': 'erp:list_venta'},
        {'name': 'Pagos', 'url': 'erp:list_pago'},
        {'name': 'Reportes', 'url': 'report_venta'},
        {'name': 'Clientes', 'url': 'erp:cliente-create'},
        {'name': 'Empresas', 'url': 'erp:empresa_list'},
        {'name': 'Inventario', 'url': 'erp:agregar_inventario'},
        {'name': 'Proveedores', 'url': 'erp:proveedor_list'},
        {'name': 'Facturas', 'url': '#'},
        {'name': 'Contactos', 'url': '#'},
        {'name': 'Ubicaciones', 'url': '#'},
    ],
    'Cliente': [
        {'name': 'Categorías', 'url': 'erp:categoria_list'},
        {'name': 'Productos', 'url': 'erp:todos_productos'},
    ],
}

SETTINGS_OPTIONS = {
    'Administrador': [
        {'name': 'Perfil', 'url': 'user:user_profile'},
        {'name': 'Configuración', 'url': 'user:user_list'},
        {'name': 'Cerrar sesión', 'url': 'logout'},
    ],
    'Cliente': [
        {'name': 'Perfil', 'url': 'user:user_profile'},
        {'name': 'Cerrar sesión', 'url': 'logout'},
    ],
}

# Categoria
CATEGORY_OPTIONS = {
    'Administrador': [
        {'name': '', 'url': 'erp:categoria_update', 'class': 'fas fa-edit'},
        {'name': '', 'url': 'erp:categoria_delete', 'class': 'fas fa-trash-alt'},
    ],
    'Cliente': []
}

CATEGORY_CREATE = {
    'Administrador': [
        {'name': 'Nuevo Registro', 'url': 'erp:categoria_create'},
    ],
    'Cliente': []
}

# Subcategoria
SUBCATEGORY_OPTIONS = {
    'Administrador': [
        {'name': '', 'url': 'erp:subcategoria_update', 'class': 'fas fa-edit'},
        {'name': '', 'url': 'erp:subcategoria_delete', 'class': 'fas fa-trash-alt'},
    ],
    'Cliente': []
}

SUBCATEGORY_CREATE = {
    'Administrador': [
        {'name': 'Nuevo Registro', 'url': 'erp:subcategoria_create'},
    ],
    'Cliente': []
}


# Productos
PRODUCT_OPTIONS = {
    'Administrador': [
        {'name': '', 'url': 'erp:producto_update', 'class': 'fas fa-edit'},
        {'name': '', 'url': 'erp:producto_delete', 'class': 'fas fa-trash-alt'},
    ],
    'Cliente': []
}


PRODUCT_CREATE = {
    'Administrador': [
        {'name': 'Nuevo Registro', 'url': 'erp:producto_create'},
    ],
    'Cliente': []
}
