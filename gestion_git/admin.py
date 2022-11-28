from django.contrib import admin
from .models import Adjudicacion, Cbu_Contribuyente, Comprobantes_de_Pago, Seccion, Embargos, Planes_de_pago

from import_export import resources
from import_export.admin import ImportExportModelAdmin
# Register your models here.

from django.contrib import admin
from .models import Adjudicacion, Cbu_Contribuyente, Comprobantes_de_Pago, Seccion, Embargos, Planes_de_pago

from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Register your models here.

class Seccion_Resource(resources.ModelResource):
    class Meta:
        model= Seccion

@admin.register (Seccion)
class Admin_Seccion(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('nombre','apellido','cuit','seccion','e_mail_agip','e_mail','direccion','telefono')
    search_fields= ('nombre','apellido','seccion')

    resource_class = Seccion_Resource

class Adjudicacion_Resource(resources.ModelResource):
    class Meta:
        model = Adjudicacion
        import_id_fields = ('adjudicacion',)

@admin.register(Adjudicacion)
class Admin_Expedientes_GIT(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('cuit','apellido_nombre', 'adjudicacion', 'solicitud',	'nro_inscripto', 
    'dominio',	'desc_adj',	'cod_imp','seccion', 'juzgado', 'oficio',	'secretaria', 
    'estado_juicio', 'f_inicio_juic', 'fecha_adj','tipo_adm',	'exp_adm', 'año_adm', 'nro_exp','año_exped',
    'imp_nominal','calle','puerta', 'piso',	'dpto',	'oficina','localidad','cod_post','date_created'
    )

    list_filter = ('seccion','cod_imp','apellido_nombre','cuit','juzgado','secretaria', 'imp_nominal')
    search_fields= ('apellido_nombre', 'cuit','adjudicacion')
    ordering = ('cuit','apellido_nombre', 'juzgado', 'secretaria', 'imp_nominal')

    resource_class = Adjudicacion_Resource


class Embargos_Resource(resources.ModelResource):
    class Meta:
        model = Embargos
        

@admin.register(Embargos)
class Admin_Embargos(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ('seccion', 'adjudicacion', 'tipo_de_embargo','clase_embargo', 'estado',
    'fecha_pedido_git', 'fecha_acreditacion','fecha_pedido_levantamiento','orden_levantamiento','fecha_levantamiento_git', 
    'dia_ingreso_embargo')

    ordering = ('tipo_de_embargo','estado','fecha_pedido_git',
    'fecha_levantamiento_git'
    )
    search_fields = ('adjudicacion',)
    autocomplete_fields= ['adjudicacion']

    resource_class= Embargos_Resource


class Planes_Resource(resources.ModelResource):
    class Meta:
        model= Planes_de_pago

@admin.register(Planes_de_pago)
class Admin_Planes_de_pago(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('seccion','adjudicacion', 'imp_actualizado', 'fecha_de_suscripcion',
    'modalidad_de_pago','cantidad_de_cuotas_plan', 'honorarios_mandatario','honorarios_procuracion', 
    'fecha_de_pago_honorarios', 'cuotas_de_honorarios', 'acredito_comprobante','estado_del_plan',
    'fecha_de_cancelacion', 'dia_ingreso_plan' 
    )

    listFilter = ('acredito_comprobante')    
    ordering =  ('fecha_de_suscripcion','cantidad_de_cuotas_plan','imp_actualizado','acredito_comprobante')
    search_fields = ('adjudicacion','seccion')
    autocomplete_fields= ['adjudicacion']

    resource_class= Planes_Resource

@admin.register(Comprobantes_de_Pago)
class Admin_Comprobante(admin.ModelAdmin):
    list_display = ('adjudicacion', 'comprobantes')

class Cbu_Resource(resources.ModelResource):
    class Meta:
        model= Cbu_Contribuyente

@admin.register(Cbu_Contribuyente)
class Admin_Cbu_Contribuyente(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('seccion', 'cuit', 'impuesto', 'adjudicacion', 'cbu','banco')
    search_fields= ('cuit','banco')

    resource_class = Cbu_Resource
