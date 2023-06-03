from django.shortcuts import render, redirect,get_object_or_404
import json
import calendar
from django.contrib.auth.decorators import login_required
from django.db.models.functions import ExtractMonth
from .models import Cliente, DetalleVenta,Proveedor,Producto,Inventario,Marca,Categoria
from .forms import VentaForm,LoginForm,ProductoForm
from django.contrib.auth import authenticate,login,logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Sum
def buscar_cliente1(request):
    if request.method == 'GET':
        nit_cliente = request.GET.get('nit', '')
        try:
            cliente = Cliente.objects.get(nit=nit_cliente)
            response = {
                'nit': cliente.nit,
                'nombre': cliente.nombre,
                'direccion': cliente.direccion,
                'telefono': cliente.telefono
            }
            return JsonResponse(response)
        except Cliente.DoesNotExist:
            mensaje_error = 'No se encontró ningún cliente con el NIT especificado.'
            response = {
                'error': mensaje_error
            }
            return JsonResponse(response, status=404)

    return JsonResponse({}, status=400)
def crear_venta1(request):
    if request.method == 'POST':
        form = VentaForm(request.POST)
        if form.is_valid():
            nit_cliente_buscar = form.cleaned_data['nit_cliente_buscar']
            cliente_existente = None

            if nit_cliente_buscar:
                # Si se proporciona un NIT, busca el cliente existente
                cliente_existente = get_object_or_404(Cliente, nit=nit_cliente_buscar)

            # Verifica si se proporcionan datos para un nuevo cliente
            nit_cliente_nuevo = form.cleaned_data['nit_cliente_nuevo']
            nombre_cliente_nuevo = form.cleaned_data['nombre_cliente_nuevo']
            direccion_cliente_nuevo = form.cleaned_data['direccion_cliente_nuevo']
            telefono_cliente_nuevo = form.cleaned_data['telefono_cliente_nuevo']

            if nit_cliente_nuevo and nombre_cliente_nuevo:
                # Si se proporcionan datos para un nuevo cliente, crea un objeto Cliente y asígnalo al detalle de venta
                cliente_nuevo = Cliente.objects.create(
                    nit=nit_cliente_nuevo,
                    nombre=nombre_cliente_nuevo,
                    direccion=direccion_cliente_nuevo,
                    telefono=telefono_cliente_nuevo
                )
                detalle_venta = form.save(commit=False)
                detalle_venta.cliente = cliente_nuevo
            elif cliente_existente:
                # Si se encontró un cliente existente, asígnalo al detalle de venta
                detalle_venta = form.save(commit=False)
                detalle_venta.cliente = cliente_existente
            else:
                # Manejar el caso de error si no se proporciona un cliente existente o datos para un nuevo cliente
                return render(request, 'detalle_venta.html', {'form': form, 'error': 'Cliente no encontrado o datos de cliente incompletos','cliente_existente': cliente_existente})

            detalle_venta.usuario = request.user
            detalle_venta.total = detalle_venta.cantidad_vendida * detalle_venta.precio_unitario

            detalle_venta.save()

            # Realizar cualquier otra operación necesaria

            return redirect('/')  # Redirigir a una página de venta exitosa

    else:
        form = VentaForm()

    return render(request, 'detalle_venta.html', {'form': form})


def buscar_cliente(request):
    nit = request.GET.get('nit')
    print("nit------------")
    print(nit)
    cliente = Cliente.objects.filter(nit=nit).first()
    data = {'cliente': None}
    if cliente:
        data['cliente'] = {
            'id': cliente.id,
            'nit': cliente.nit,
            'nombre': cliente.nombre,
            'direccion': cliente.direccion,
            'telefono': cliente.telefono
            # Agrega más campos del cliente si los necesitas
        }
    else:
        print("Cliente no encontrado")    
    print("datos-----------------------------------------")
    print(data['cliente'])
    return JsonResponse(data)
    
def crear_venta(request):
    if request.method == 'POST':
        form = VentaForm(request.POST)
        if form.is_valid():
            nit_cliente_buscar = form.cleaned_data['nit_cliente_buscar']
            cliente_existente = None
            # Obtener la cantidad vendida y el producto de la venta
            cantidad_vendida = form.cleaned_data['cantidad_vendida']
            producto_vendido = form.cleaned_data['producto']

            if nit_cliente_buscar:
                # Si se proporciona un NIT, busca el cliente existente
                cliente_existente = get_object_or_404(Cliente, nit=nit_cliente_buscar)

            # Verifica si se proporcionan datos para un nuevo cliente
            nit_cliente_nuevo = form.cleaned_data['nit_cliente_nuevo']
            nombre_cliente_nuevo = form.cleaned_data['nombre_cliente_nuevo']
            direccion_cliente_nuevo = form.cleaned_data['direccion_cliente_nuevo']
            telefono_cliente_nuevo = form.cleaned_data['telefono_cliente_nuevo']

            if nit_cliente_nuevo and nombre_cliente_nuevo:
                # Si se proporcionan datos para un nuevo cliente, crea un objeto Cliente y asígnalo al detalle de venta
                cliente_nuevo = Cliente.objects.create(
                    nit=nit_cliente_nuevo,
                    nombre=nombre_cliente_nuevo,
                    direccion=direccion_cliente_nuevo,
                    telefono=telefono_cliente_nuevo
                )
                detalle_venta = form.save(commit=False)
                detalle_venta.cliente = cliente_nuevo
            elif cliente_existente:
                # Si se encontró un cliente existente, asígnalo al detalle de venta
                detalle_venta = form.save(commit=False)
                detalle_venta.cliente = cliente_existente
            else:
                # Manejar el caso de error si no se proporciona un cliente existente o datos para un nuevo cliente
                return render(request, 'prueba.html', {'form': form, 'error': 'Cliente no encontrado o datos de cliente incompletos','cliente_existente': cliente_existente})

            detalle_venta.usuario = request.user
            detalle_venta.total = detalle_venta.cantidad_vendida * detalle_venta.precio_unitario

            detalle_venta.save()
             # Actualizar la cantidad de inventario del producto vendido
            inventario = Inventario.objects.get(producto=producto_vendido)
            inventario.cantidad_inventario -= cantidad_vendida
            inventario.save()

            # Realizar cualquier otra operación necesaria

            return redirect('/')  # Redirigir a una página de venta exitosa

    else:
        form = VentaForm()

    return render(request, 'prueba.html', {'form': form})



def obtener_precio_venta(request):
    producto_id = request.GET.get('producto')
    producto = Producto.objects.filter(id=producto_id).first()

    if producto:
        data = {
            'precioVenta': producto.precioVenta
        }
    else:
        data = {}

    return JsonResponse(data)

#LOGIN 
def login_view(request):
    if request.method=='POST':
        form=LoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            print(request.POST)
            user=authenticate(request,username=username,password=password)
            print(user)
            if user is not None:
                login(request,user)
                return redirect('home')
            else:
                error_message='Credenciales Incorrectas, Verifique por favor'
                # form=LoginForm()
                return render(request,'login.html',{'form':form,'error_message':error_message})
    else:
        form=LoginForm() 

    return render(request,'login.html',{'form':form})  
def logout_view(request):
    logout(request)
    return redirect('/')
def home(request):
    ventas_por_mes = DetalleVenta.objects.annotate(mes=ExtractMonth('fecha_venta')).values('mes').annotate(total_ganancias=Sum('total')).order_by('mes')

    ventas_por_mes_json = [
        {   
            # 'mes': venta['mes'],
            'mes': calendar.month_name[venta['mes']],
            'total_ganancias': float(venta['total_ganancias'])  # Convertir Decimal a float
        }
        for venta in ventas_por_mes
    ]

    # Obtener la fecha y hora actual en la zona horaria del proyecto
    now = timezone.now()

    # Calcular la fecha y hora límite para productos por vencer (10 días a partir de ahora)
    limite = now + timedelta(days=10)

    # Obtener los productos por vencer en la fecha límite
    productos_por_vencer = Inventario.objects.filter(fecha_vencimiento__lte=limite)

    context = {
        'productos_por_vencer': productos_por_vencer,
         'ventas_por_mes_json': json.dumps(ventas_por_mes_json)
    }
    return render(request,'home.html',context)

def dashboard(request):
    ventas_por_mes = DetalleVenta.objects.annotate(mes=ExtractMonth('fecha_venta')).values('mes').annotate(total_ganancias=Sum('total')).order_by('mes')

    ventas_por_mes_json = [
        {
            # 'mes': venta['mes'],
            'mes': calendar.month_name[venta['mes']],
            'total_ganancias': float(venta['total_ganancias'])  # Convertir Decimal a float
        }
        for venta in ventas_por_mes
    ]

    context = {
        'ventas_por_mes_json': json.dumps(ventas_por_mes_json)
    }

    return render(request, 'dashboard.html', context)

#CONTACTOS
def clientes(request):
    cliente=Cliente.objects.all()

    return render(request,'contactos/clientes.html',{'cliente':cliente})
def proveedores(request):
    proveedor=Proveedor.objects.all()
    return render(request,'contactos/proveedores.html',{'proveedor':proveedor})

#INVENTARIO
def ver_inventario(request):
    return render(request,'Inventario/inventario.html')
def realizarCompra(request):
    productos_bajo_inventario = Inventario.objects.filter(cantidad_inventario__lt=10)

    context = {
        'productos_bajo_inventario': productos_bajo_inventario
    }

    return render(request, 'Inventario/realizarCompra.html', context)

#PRODUCTOS
def agregarProducto(request):
    if request.method=='POST':
        form=ProductoForm(request.POST)
        print("-----------------------")
        print(request.POST)
        if form.is_valid():
            producto = form.save(commit=False)
            # Obtener proveedor, categoria y marca seleccionados en el formulario
            proveedor_id = request.POST.get('proveedor')
            categoria_id = request.POST.get('categoria')
            marca_id = request.POST.get('marca')
            proveedor = Proveedor.objects.get(pk=proveedor_id)
            categoria = Categoria.objects.get(pk=categoria_id)
            marca = Marca.objects.get(pk=marca_id)
            # Asignar proveedor, categoria y marca al producto
            producto.proveedor = proveedor
            producto.categoria = categoria
            producto.marca = marca
            producto.save()
            # print("datos guardados")
            # print(producto)
            return redirect('home')   
    else:
        form=ProductoForm()        
    return render(request,'productos/agregarProducto.html',{'form':form})

def laboratorios(request):
    return render(request,'productos/laboratorios.html')

@login_required(login_url='login') 
def listaProductos(request):
    lista_producto=Producto.objects.all().order_by('nombre')
    context={'lista_producto':lista_producto}
    return render(request,'productos/listaProductos.html',context)

#REPORTES
def informeCompras(request):
    return render(request,'reportes/informeCompras.html')
def informeVentas(request):
    return render(request,'reportes/informeVentas.html')

#VENDER
def consultarVenta(request):
    return render(request,'vender/consultarVenta.html')
def listaVenta(request):
    # Obtener la fecha y hora actual en la zona horaria del proyecto
    now = timezone.now()

    # Calcular la fecha y hora límite para productos por vencer (10 días a partir de ahora)
    limite = now + timedelta(days=10)

    # Obtener los productos por vencer en la fecha límite
    productos_por_vencer = Inventario.objects.filter(fecha_vencimiento__lte=limite)

    context = {
        'productos_por_vencer': productos_por_vencer
    }
    return render(request,'home.html',context)


def realizarVenta(request):
    return render(request,'vender/realizarVenta.html')

#ADMINISTRADOR
def register_view(request):

    return render(request,'administrador/register.html')





