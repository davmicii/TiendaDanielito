Tienda Danielito 1.0


Proyecto personal realizado para llevar el control de las ventas, gastos e inventario de la TiendaDanielito.



Glosario de Términos:
UA: Usuario autorizado
UNA: Usuario no autorizado



Tecnologías:
- Python
- Django
- PostgreSQL

General:
Cuando se completa el proceso de autenticación se redirijirá a la vista de dashboard. Aquí según sea el grupo al que
pertenece un usuario se mostrarán las opciones correspondientes y se bloquearán o habilitarán las rutas respectivas.



Módulos terminados:
- Usuarios
Permite la creación de usuarios mediante un UA.
Permite el acceso al sistema a usuarios registrados y acceso a determinadas vistas.
Permite la creación de grupos y asignación de usuarios a determinado grupo.
Permite visualizar el perfil a todos los usuarios.


- Categorías, Subcateogorías y Productos
Permite el CRUD de todos estos módulos mediante un UA.
Permite solo la visualización a un UNA.


- Clientes, Empresas, Proveedores
Permite el CRUD de los módulos mediante un UA.
Un UNA no tiene acceso a los módulos.


- Detalle Producto, Todos los productos
Permite visualizar el detalle de un producto a todos los usuarios.


- Inventario
Permite asignar el stock o inventario a un producto, solo los UA. 


- Ventas
Permite el CRUD y descarga de una factura de venta, solo para UA
Los UNA no tienen acceso.


- Reportes
Permite visualizar y descargar los reportes de ventas, se pueden filtrar por fechas.



Estas son la mayoría de las funciones que realiza el sistema.


Siguientes mejoras TiendaDanielito 1.1:
- Mejorar el proceso de gestión de inventario.
- Completar el módulo de pagos, tiene similitud con el de ventas.
- Completar el módulo de facturas, cuando se hace una venta, guardar el PDF también en ese módulo, separarlos en facturas de
  ventas y pagos.







