from cProfile import label
from email.policy import default
#from attr import fields
from django.contrib.admin.widgets import AutocompleteSelect
from django.contrib import admin

#Login y Registracion
from django.contrib.admin.helpers import ActionForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from django import forms
from django.forms import ModelForm, inlineformset_factory, widgets
from django.forms import ClearableFileInput

from gestion_git.models import Embargos, Planes_de_pago, Seccion, Adjudicacion, Comprobantes_de_Pago, Patente

# Crear formulario de usuario

class Crear_Formulario_User(UserCreationForm):
    class Meta:
        model = User 
        fields= ['username','first_name','last_name','email', 'password1', 'password2']



#Formulario Seccion Mandatario
class Crear_Mandatario_Form(ModelForm):
    cuit= forms.CharField(max_length= 13, label='CUIT')
    class Meta:
        model= Seccion
        fields = ('nombre', 'apellido', 'cuit', 'seccion', 
        'e_mail', 'e_mail_agip','direccion', 'telefono')


#Formulario Expedientes GIT

class Crear_Expediente_Git_Form(ModelForm):
    class Meta:
        model= Adjudicacion

        fields= ('cuit','apellido_nombre','adjudicacion','solicitud','nro_inscripto','dominio',
            'desc_adj','cod_imp','seccion','mandatario','juzgado','oficio','secretaria',
            'estado_juicio','f_inicio_juic','fecha_adj','tipo_adm','exp_adm','año_adm',
            'nro_exp','año_exped','imp_nominal','calle','puerta','piso','dpto','oficina',
            'localidad','cod_post','const_deuda'
        )

class Formulario_expedientes_Git(ModelForm):
    class Meta:
        model= Adjudicacion
        
        fields = (
            'cuit','apellido_nombre','adjudicacion','solicitud','nro_inscripto','dominio',
            'desc_adj','cod_imp','seccion','mandatario','juzgado','oficio','secretaria',
            'estado_juicio','f_inicio_juic','fecha_adj','tipo_adm','exp_adm','año_adm',
            'nro_exp','año_exped','imp_nominal','calle','puerta','piso','dpto','oficina',
            'localidad','cod_post','const_deuda'
        )

        widgets = {
            'adjudicacion': AutocompleteSelect (
                Adjudicacion._meta.get_field('adjudicacion').remote_field, 
                admin.site,
            )
        }

Formulario_expedientes_Git_Set = inlineformset_factory(
    Seccion,
    Adjudicacion,
    Formulario_expedientes_Git,
    can_delete=False,
    max_num=1,
)


#Formulario Nuevo Plan de Pagos

class Formulario_planes(ModelForm):
    fecha_de_suscripcion= forms.DateField(label='Fecha de suscripción',widget=forms.DateInput(attrs={'type':'date'}))
    fecha_de_pago_honorarios = forms.DateField(label='Fecha de pago de honorarios',required=False,widget=forms.DateInput(attrs={'type':'date'}))
    imp_actualizado= forms.CharField(label= 'Importe actualizado')
    honorarios_procuracion= forms.CharField(label= 'Honorarios Procuración', initial= '7867.58')
    honorarios_mandatario = forms.CharField(label='Honorarios Mandatario', initial='22212.81')
   
    class Meta:
        model = Planes_de_pago
        fields = ('adjudicacion','imp_actualizado','fecha_de_suscripcion', 'archivo_plan',
        'modalidad_de_pago','cantidad_de_cuotas_plan','honorarios_mandatario','honorarios_procuracion',
        'fecha_de_pago_honorarios','cuotas_de_honorarios','estado_del_plan','comprobantes','email','celular'
        )
        
        widgets= {
            'comprobantes': ClearableFileInput(attrs={'multiple': True}),
        }

    #    widgets = {
    #        'adjudicacion': AutocompleteSelect (
    #            Planes_de_pago._meta.get_field('adjudicacion').remote_field, 
    #            admin.site,
    #        )
    #    }

Formulario_Planes_Git_Set = inlineformset_factory(
    Adjudicacion,
    Planes_de_pago,
    Formulario_planes,
    can_delete=False,
    max_num=1,
)

class Formulario_comprobantes(forms.ModelForm):
    class Meta:
        model = Comprobantes_de_Pago
        fields = ('adjudicacion', 'comprobantes')
        widgets= {
            'comprobantes': ClearableFileInput(attrs={'multiple': True}),
        }


# Formulario Nuevo Embargo

class Formulario_embargo(ModelForm):
    fecha_pedido_git= forms.DateField(label= 'Fecha de pedido en GIT',widget=forms.DateInput(attrs={'type':'date'}))
    fecha_acreditacion = forms.DateField(label='Fecha de acreditación en juicio',required=False,widget=forms.DateInput(attrs={'type':'date'}))
    fecha_pedido_levantamiento = forms.DateField(label='Fecha pedido lev. en juicio',required=False, widget=forms.DateInput(attrs={'type':'date'}))
    fecha_levantamiento_git = forms.DateField(label='Fecha de lev. en GIT',required=False,widget=forms.DateInput(attrs={'type':'date'}))
    adjudicacion = forms.ModelChoiceField(queryset=Adjudicacion.objects.filter(seccion_id=147))

    class Meta:
        model = Embargos
        fields = ('id','adjudicacion','tipo_de_embargo','clase_embargo','monto_embargado',
        'estado','fecha_pedido_git','fecha_acreditacion','fecha_pedido_levantamiento',
        'orden_levantamiento','fecha_levantamiento_git','oficio_embargo', 'oficio_lev_embargo'
        )
        
        #widgets = {
        #    'adjudicacion': AutocompleteSelect (
        #        Embargos._meta.get_field('adjudicacion').remote_field,
        #        admin.site,
        #    )
        #}

Formulario_Embargo_Git_Set = inlineformset_factory(
    Adjudicacion,
    Embargos,
    Formulario_embargo,
    can_delete=False,
    max_num=1,
)

class Formulario_patente(ModelForm):
    seccion = forms.ModelChoiceField(queryset=Seccion.objects.filter())

    class Meta:
        model = Patente
        fields = ('id','seccion','titular','cuit','dominio')
        