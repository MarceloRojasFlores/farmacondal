from django import forms
from .models import DetalleVenta, Cliente,CustomUser,Rol,Producto,Categoria,Proveedor
from django.contrib.auth.forms import UserCreationForm
class UserRegistrationForm(UserCreationForm):
    rol = forms.ModelChoiceField(queryset=Rol.objects.all())
    DNI = forms.CharField(max_length=255)
    telefono = forms.IntegerField()

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'rol', 'DNI', 'telefono', 'password1', 'password2')    

class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(
                            attrs={'type':'text','class':'form-control','id':'floatingInput','placeholder':'nombre de usuario'}))
    password=forms.CharField(widget=forms.PasswordInput(
                            attrs={'type':'password','class':'form-control','id':'floatingPassword','placeholder':'Password'}))
    
class ProductoForm(forms.ModelForm):
    categoria = forms.ModelChoiceField(queryset=Categoria.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model=Producto
        exclude=['cantidad_vistas']
        fields='__all__'
        widgets={
            'nombre':forms.TextInput(attrs={'class':'form-control','placeholder':'Ingrese el nombre del producto'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00', 'step': '0.01'}),
            'precioVenta': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00', 'step': '0.01'}),
            
        }
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['categoria'].empty_label = 'Seleccione una categoría'
            self.fields['proveedor'].empty_label='Seleccione un proveedor'
            self.fields['marca'].empty_label='Seleccione un laboratorio'

class VentaForm(forms.ModelForm):
    cliente_existente = forms.ModelChoiceField(queryset=Cliente.objects.all(), required=False)
    nit_cliente_buscar = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={'placeholder': 'Buscar cliente por NIT','id':'id_nit_cliente_buscar','name':'id_nit_cliente_buscar'}))
    nit_cliente_nuevo = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={'placeholder': 'NIT del nuevo cliente'}))
    nombre_cliente_nuevo = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'placeholder': 'Nombre del nuevo cliente'}))
    direccion_cliente_nuevo = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'placeholder': 'Dirección del nuevo cliente'}))
    telefono_cliente_nuevo = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={'placeholder': 'Teléfono del nuevo cliente'}))

    class Meta:
        model = DetalleVenta
        fields = ['producto', 'cantidad_vendida', 'precio_unitario','total']

    def clean(self):
        cleaned_data = super().clean()
        nit_cliente_nuevo = cleaned_data.get('nit_cliente_nuevo')
        nombre_cliente_nuevo = cleaned_data.get('nombre_cliente_nuevo')

        if nit_cliente_nuevo and not nombre_cliente_nuevo:
            self.add_error('nombre_cliente_nuevo', 'Ingrese el nombre del nuevo cliente')
        elif nombre_cliente_nuevo and not nit_cliente_nuevo:
            self.add_error('nit_cliente_nuevo', 'Ingrese el NIT del nuevo cliente')

        return cleaned_data
