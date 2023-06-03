from django.urls import path
from . import views
urlpatterns = [
    path('register/',views.register_view,name='register'),
    path("crear_venta/", views.crear_venta1, name='crear_venta1'),
    path('buscar_cliente1/', views.buscar_cliente1, name='buscar_cliente1'),
    path('obtener_precio_venta/', views.obtener_precio_venta, name='obtener_precio_venta'),

    path('buscar_cliente/',views.buscar_cliente,name='buscar_cliente'),
    path("venta/",views.crear_venta,name='venta'),


    path('',views.login_view, name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('home/',views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    path('inventario/',views.ver_inventario,name='inventario'),


    path('contactos/clientes/',views.clientes, name='clientes'),
    path('contactos/proveedores/',views.proveedores, name='proveedores'),

     path('compras/realizarCompra/',views.realizarCompra, name='realizarCompra'),

    path('productos/agregarProducto/',views.agregarProducto, name='agregarProducto'),
     path('productos/laboratorios/',views.laboratorios, name='laboratorios'),
      path('productos/listaProductos/',views.listaProductos, name='listaProductos'),

    path('reportes/informeCompras/',views.informeCompras, name='informeCompras'),
    path('reportes/informeVentas/',views.informeVentas, name='informeVentas'),


    path('vender/consultarVenta/',views.consultarVenta, name='consultarVenta'),
      path('vender/listaVenta/',views.listaVenta, name='listaVenta'),
      path('vender/realizarVenta/',views.realizarVenta, name='realizarVenta'),

]