from django.contrib import admin
from django.contrib.admin import site
from app.core.erp.models import Categoria


admin.site.register(Categoria)