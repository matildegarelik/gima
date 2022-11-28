#from attr import field
import django_filters
from .models import *
from django import forms
from django_filters import CharFilter
from django_filters import DateFilter

class Expediente_Git_Filtro(django_filters.FilterSet):
    apellido_nombre = CharFilter(field_name ='apellido_nombre', label= 'Demandado',lookup_expr='icontains')
    nro_inscripto = CharFilter(label='Nro. Inscripto')
    dominio=CharFilter(field_name='dominio', label='Dominio', lookup_expr='icontains')
    nro_inscripto=CharFilter(field_name='nro_inscripto', label='Nro. Inscripto', lookup_expr='icontains')
    
    class Meta:
        model = Adjudicacion
        fields = ['seccion','cuit', 'apellido_nombre','adjudicacion', 'nro_inscripto', 
        'dominio', 'juzgado', 'secretaria', 'nro_exp', 'año_exped','cod_imp', 'date_created']

class Embargos_Git_Filtro(django_filters.FilterSet):
    adjudicacion= CharFilter(field_name="adjudicacion", label= 'Nro. Adjudicacón', lookup_expr='icontains')
    dia_ingreso_embargo_desde = DateFilter(field_name='fecha_pedido_git',lookup_expr='gte',label='Fecha de embargo desde', widget=forms.DateInput(attrs={'type':'date'}))
    dia_ingreso_embargo_hasta = DateFilter(field_name='fecha_pedido_git',lookup_expr='lte',label='Fecha de embargo hasta',widget=forms.DateInput(attrs={'type':'date'}))

    class Meta:
        model = Embargos
        fields = ('seccion', 'adjudicacion', 'tipo_de_embargo','clase_embargo','estado',
        'fecha_pedido_git','dia_ingreso_embargo')
        exclude = ['oficio_embargo', 'oficio_lev_embargo']

class Planes_Git_Filtro(django_filters.FilterSet):
    adjudicacion= CharFilter(field_name="adjudicacion", label= 'Nro. Adjudicacón',lookup_expr='icontains')
    fecha_de_suscripcion_desde= DateFilter(field_name='fecha_de_suscripcion', label='Fecha de Suscripción desde', lookup_expr='gte',widget=forms.DateInput(attrs={'type':'date'}))
    fecha_de_suscripcion_hasta= DateFilter(field_name='fecha_de_suscripcion', label='Fecha de Suscripción hasta', lookup_expr='lte',widget=forms.DateInput(attrs={'type':'date'}))

    class Meta:
        model = Planes_de_pago
        fields = ('seccion','adjudicacion','fecha_de_suscripcion','cantidad_de_cuotas_plan',
        'estado_del_plan', 'fecha_de_cancelacion','dia_ingreso_plan')
        exclude = ['archivo_plan','comprobantes']

class Cbu_contribuyente_Filtro(django_filters.FilterSet):
    adjudicacion= CharFilter(field_name="adjudicacion", label= 'Nro. Adjudicación',lookup_expr='icontains')
    cuit= CharFilter(field_name="cuit", label= 'CUIT',lookup_expr='icontains')

    class Meta:
        model= Cbu_Contribuyente
        fields = ('seccion', 'cuit', 'adjudicacion', 'cbu', 'banco')