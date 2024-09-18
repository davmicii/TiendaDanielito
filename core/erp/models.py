from datetime import datetime

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.forms import model_to_dict

from config.settings import MEDIA_URL, STATIC_URL
from core.erp.choices import gender_choices


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre', unique=True)
    imagen_categoria = models.ImageField(upload_to='categorias/%Y/%m/%d', null=True, blank=True)

    def __str__(self):
        return self.nombre

    def get_image(self):
        if self.imagen_categoria:
            return '{}{}'.format(MEDIA_URL, self.imagen_categoria)
        return '{}{}'.format(STATIC_URL, 'img/categorias/default.svg')

    def tojson(self):
        item = model_to_dict(self)
        return item

    class Meta:
        app_label = 'erp'
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        db_table = 'categoria'
        ordering = ['id']


class SubCategoria(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Categoria')
    nombre = models.CharField(max_length=100, verbose_name='Nombre', unique=True)
    imagen_subcategoria = models.ImageField(upload_to='subcategorias/%Y/%m/%d', null=True, blank=True)

    def __str__(self):
        return self.categoria.nombre

    def get_image(self):
        if self.imagen_subcategoria:
            return '{}{}'.format(MEDIA_URL, self.imagen_subcategoria)
        return '{}{}'.format(STATIC_URL, 'img/subcategorias/default.svg')

    def tojson(self):
        item = model_to_dict(self)
        return item

    class Meta:
        app_label = 'erp'
        verbose_name = 'SubCategoria'
        verbose_name_plural = 'SubCategorias'
        db_table = 'subcategoria'
        ordering = ['id']


class Empresa(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre', unique=True)
    direccion = models.CharField(max_length=100, null=True, blank=True, verbose_name='Dirección')
    imagen_empresa = models.ImageField(upload_to='empresas/%Y/%m/%d', null=True, blank=True)

    def __str__(self):
        return self.nombre

    def get_image(self):
        if self.imagen_empresa:
            return '{}{}'.format(MEDIA_URL, self.imagen_empresa)
        return '{}{}'.format(STATIC_URL, 'img/empresas/default.svg')

    def tojson(self):
        item = model_to_dict(self)
        return item

    class Meta:
        app_label = 'erp'
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
        db_table = 'empresa'
        ordering = ['id']


class Producto(models.Model):
    subcategoria = models.ForeignKey(SubCategoria, on_delete=models.CASCADE, null=True, blank=True, verbose_name='SubCategoria')
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Empresa')
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    descripcion = models.CharField(max_length=200, null=True, blank=True, verbose_name='Descripcion')
    precio = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2)
    imagen_producto = models.ImageField(upload_to='productos/%Y/%m/%d', null=True, blank=True)

    def __str__(self):
        return self.nombre

    def get_image(self):
        if self.imagen_producto:
            return '{}{}'.format(MEDIA_URL, self.imagen_producto)
        return '{}{}'.format(STATIC_URL, 'img/productos/default.svg')

    def tojson(self):
        item = model_to_dict(self)
        item['subcategoria'] = self.subcategoria.tojson()
        item['imagen_producto'] = self.get_image()
        item['precio'] = format(self.precio, '.2f')
        return item

    class Meta:
        app_label = 'erp'
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        db_table = 'producto'
        ordering = ['id']


# class Precio(models.Model):
#     producto = models.ForeignKey(Producto, on_delete=models.CASCADE, verbose_name='Producto')
#     fecha = models.DateTimeField(auto_now_add=True)
#     precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Precio')
#     estados = (
#         ('SI', 'si'),
#         ('NO', 'no')
#     )
#     bool_precio_actual = models.CharField(max_length=10, choices=estados, default='SI', verbose_name='Precio Actual')
#
#     def __str__(self):
#         return self.precio
#
#     class Meta:
#         app_label = 'erp'
#         verbose_name = 'Precio'
#         verbose_name_plural = 'Precios'
#         db_table = 'precio'
#         ordering = ['id']


class Inventario(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, verbose_name='Producto')
    cantidad = models.IntegerField(verbose_name="Cantidad", default=0)
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.producto.nombre

    def tojson(self):
        item = model_to_dict(self)
        return item

    class Meta:
        app_label = 'erp'
        verbose_name = 'Inventario'
        verbose_name_plural = 'Inventarios'
        db_table = 'inventario'
        ordering = ['id']


class Proveedor(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, verbose_name='Empresa')
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    telefono = models.CharField(max_length=11, null=True, blank=True, verbose_name='Teléfono')
    dias_visita = (
        ('lunes', 'Lunes'),
        ('martes', 'Martes'),
        ('miercoles', 'Miércoles'),
        ('jueves', 'Jueves'),
        ('viernes', 'Viernes'),
        ('sabado', 'Sábado'),
        ('domingo', 'Domingo'),
        ('no', 'Sin definir'),
    )
    bool_dias_visita = ArrayField(
        models.CharField(max_length=20, choices=dias_visita, default='no'),
        verbose_name='Días de Visita'
    )

    def __str__(self):
        return self.nombre

    def tojson(self):
        item = model_to_dict(self)
        return item

    class Meta:
        app_label = 'erp'
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        db_table = 'proveedor'
        ordering = ['id']


class Contacto(models.Model):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Proveedor')
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Empresa')
    #nombre = models.CharField(max_length=100, null=True, blank=True, verbose_name='Nombre')
    telefono_pr = models.CharField(max_length=10, null=True, blank=True, verbose_name='Teléfono Principal')
    telefono_se = models.CharField(max_length=10, null=True, blank=True, verbose_name='Telefono Secundario')
    correo = models.CharField(max_length=100, null=True, blank=True, verbose_name='Correo', unique=True)

    def __str__(self):
        return self.proveedor.nombre

    class Meta:
        app_label = 'erp'
        verbose_name = 'Contacto'
        verbose_name_plural = 'Contactos'
        db_table = 'contacto'
        ordering = ['id']


class UbicacionProducto(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, verbose_name='Producto')
    referencia = models.CharField(max_length=100, null=True, blank=True)
    imagen_referencia = models.ImageField(upload_to='ubicacion/%Y/%m/%d', null=True, blank=True)

    def __str__(self):
        return self.referencia

    def get_image(self):
        if self.imagen_referencia:
            return '{}{}'.format(MEDIA_URL, self.imagen_referencia)
        return '{}{}'.format(STATIC_URL, 'img/ubicacion_productos/default.svg')


    class Meta:
        app_label = 'erp'
        verbose_name = 'Ubicación de Producto'
        verbose_name_plural = 'Ubicación de Productos'
        db_table = 'ubicacion_producto'
        ordering = ['id']


class Factura(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, verbose_name='Empresa')
    imagen_factura = models.ImageField(upload_to='factura/%Y/%m/%d', null=True, blank=True)

    def __str__(self):
        return self.empresa.nombre

    def get_image(self):
        if self.imagen_factura:
            return '{}{}'.format(MEDIA_URL, self.imagen_factura)
        return '{}{}'.format(STATIC_URL, 'img/facturas/default.svg')

    class Meta:
        app_label = 'erp'
        verbose_name = 'Factura'
        verbose_name_plural = 'Facturas'
        db_table = 'factura'
        ordering = ['id']


class Cliente(models.Model):
    nombres = models.CharField(max_length=150, verbose_name='Nombres')
    apellidos = models.CharField(max_length=150, verbose_name='Apellidos')
    cedula = models.CharField(max_length=10, unique=True, verbose_name='Cédula')
    fecha_nacimiento = models.DateField(verbose_name='Fecha de nacimiento')
    direccion = models.CharField(max_length=150, null=True, blank=True, verbose_name='Dirección')
    genero = models.CharField(max_length=10, choices=gender_choices, default='male', verbose_name='Sexo')

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

    def tojson(self):
        item = model_to_dict(self)
        item['genero'] = {'id': self.genero, 'name': self.get_genero_display()}
        item['fecha_nacimiento'] = self.fecha_nacimiento.strftime('%Y-%m-%d')
        return item

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        db_table = 'cliente'
        ordering = ['id']


class Venta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name='Cliente')
    fecha_venta = models.DateField(default=datetime.now)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    iva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.cliente.nombres

    def tojson(self):
        item = model_to_dict(self)
        item['cliente'] = self.cliente.tojson()
        item['subtotal'] = format(self.subtotal, '.2f')
        item['iva'] = format(self.iva, '.2f')
        item['total'] = format(self.total, '.2f')
        item['fecha_venta'] = self.fecha_venta.strftime('%Y-%m-%d')
        item['det'] = [i.tojson() for i in self.detalleventa_set.all()]
        return item

    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        db_table = 'venta'
        ordering = ['id']


class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    precio = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cantidad = models.IntegerField(default=0)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.producto.nombre

    def tojson(self):
        item = model_to_dict(self, exclude=['venta'])
        item['producto'] = self.producto.tojson()
        item['precio'] = format(self.precio, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        return item

    class Meta:
        verbose_name = 'Detalle de Venta'
        verbose_name_plural = 'Detalle de Ventas'
        db_table = 'detalle_venta'
        ordering = ['id']


class Pago(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, verbose_name='Empresa')
    fecha_pago = models.DateField(default=datetime.now)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.total

    def tojson(self):
        item = model_to_dict(self, exclude=['venta'])
        item['empresa'] = self.empresa.tojson()
        item['fecha_pago'] = self.fecha_pago.strftime('%Y-%m-%d')
        item['total'] = format(self.total, '.2f')
        return item

    class Meta:
        verbose_name = 'Pago'
        verbose_name_plural = 'Pagos'
        db_table = 'pago'
        ordering = ['id']
