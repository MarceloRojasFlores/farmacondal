from django.contrib import admin
from .models import CustomUser,Rol,DetalleVenta,Cliente,Producto,Proveedor,Categoria,Marca,Inventario
# Register your models here.

class DetalleVentaAdmin(admin.ModelAdmin):
    list_display = ('producto', 'cantidad_vendida', 'precio_unitario', 'cliente', 'usuario', 'fecha_venta', 'total')
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'precioVenta', 'proveedor', 'marca', 'categoria')


class InventarioAdmin(admin.ModelAdmin):
    list_display=['producto','cantidad_inventario','fecha_vencimiento']
    search_fields=['producto__nombre__icontains']

admin.site.register(DetalleVenta, DetalleVentaAdmin)
admin.site.register(CustomUser)
admin.site.register(Rol)

admin.site.register(Cliente)
admin.site.register(Producto,ProductoAdmin)
admin.site.register(Proveedor)
admin.site.register(Categoria)
admin.site.register(Marca)
admin.site.register(Inventario,InventarioAdmin)