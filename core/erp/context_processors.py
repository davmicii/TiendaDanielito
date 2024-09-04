from .navigation import *


# Opciones del dashboard
def user_navigation(request):
    if request.user.is_authenticated:
        for group in request.user.groups.all():
            if group.name in NAVIGATION_OPTIONS:
                return {'navigation_options': NAVIGATION_OPTIONS[group.name]}
    return {'navigation_options': []}


# Opciones del usuario
def user_settings_navigation(request):
    if request.user.is_authenticated:
        for group in request.user.groups.all():
            if group.name in SETTINGS_OPTIONS:
                return {'settings_options': SETTINGS_OPTIONS[group.name]}
    return {'settings_options': []}


# Acciones de categoría
def category_options(request):
    if request.user.is_authenticated:
        for group in request.user.groups.all():
            if group.name in CATEGORY_OPTIONS:
                return {'category_options': CATEGORY_OPTIONS[group.name]}
    return {'category_options': []}


# Crear categoría
def category_create(request):
    if request.user.is_authenticated:
        for group in request.user.groups.all():
            if group.name in CATEGORY_CREATE:
                return {'category_create': CATEGORY_CREATE[group.name]}
    return {'category_create': []}


# Opciones de subcategoría
def subcategory_options(request):
    if request.user.is_authenticated:
        for group in request.user.groups.all():
            if group.name in SUBCATEGORY_OPTIONS:
                return {'subcategory_options': SUBCATEGORY_OPTIONS[group.name]}
    return {'subcategory_options': []}


# Crear subcategoría
def subcategory_create(request):
    if request.user.is_authenticated:
        for group in request.user.groups.all():
            if group.name in SUBCATEGORY_CREATE:
                return {'subcategory_create': SUBCATEGORY_CREATE[group.name]}
    return {'subcategory_create': []}


# Opciones de producto
def product_options(request):
    if request.user.is_authenticated:
        for group in request.user.groups.all():
            if group.name in PRODUCT_OPTIONS:
                return {'product_options': PRODUCT_OPTIONS[group.name]}
    return {'product_options': []}


# Crear producto
def product_create(request):
    if request.user.is_authenticated:
        for group in request.user.groups.all():
            if group.name in PRODUCT_CREATE:
                return {'product_create': PRODUCT_CREATE[group.name]}
    return {'product_create': []}
