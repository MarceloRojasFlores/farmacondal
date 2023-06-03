from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password

class Rol(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre


class CustomUser(AbstractUser):
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE, blank=True, null=True)
    DNI = models.CharField(max_length=255, null=True, blank=True)
    telefono = models.PositiveSmallIntegerField(null=True, blank=True)

    class Meta:
        verbose_name = 'CustomUser'
        verbose_name_plural = 'CustomUsers'

    def __str__(self):
        return f"{self.username}-{self.rol.nombre}"
    def save(self, *args, **kwargs):
        if not self.pk:
            # Si el usuario es nuevo (no tiene clave primaria),
            # establece la contraseña utilizando make_password
            self.password = make_password(self.password)

        super().save(*args, **kwargs)    


class Cliente(models.Model):
    nit = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=255)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)
    def __str__(self):
        return self.nombre+"-"+self.nit


class Proveedor(models.Model):
    nombre = models.CharField(max_length=255)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)
    def __str__(self):
        return self.nombre

class Categoria(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(null=True,blank=True)
    def __str__(self):
        return self.nombre
    
class Marca(models.Model):
    nombre = models.CharField(max_length=255,unique=True)
    descripcion = models.TextField(null=True,blank=True)
    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=255,unique=True)
    descripcion = models.TextField(null=True,blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    precioVenta=models.DecimalField(max_digits=10,decimal_places=2)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE)
    cantidad_vistas = models.PositiveIntegerField(default=0)

    def incrementar_vistas(self):
        self.cantidad_vistas += 1
        self.save()
    def __str__(self):
        return self.nombre

# class Venta(models.Model):
#     fecha_venta = models.DateTimeField(auto_now_add=True)
#     cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
#     empleado = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

class DetalleVenta(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad_vendida = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, blank=True, null=True)
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    fecha_venta = models.DateTimeField(auto_now=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    def __str__(self):
        return self.cliente.nombre

class Inventario(models.Model):
    producto = models.OneToOneField(Producto, on_delete=models.CASCADE)
    cantidad_inventario = models.PositiveIntegerField(default=0)
    fecha_vencimiento=models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return self.producto.nombre+" Cantidad:"+str(self.cantidad_inventario)
