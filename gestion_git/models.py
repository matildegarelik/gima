from django.db import models
from tokenize import blank_re
from django.db import models
from django.db.models.deletion import CASCADE, PROTECT, RESTRICT, SET_NULL
from django.forms import EmailField
from django.db.models.fields.related import ForeignKey
from django.db.models.fields.files import FileField
from .choices import *
from django.contrib.auth.models import User

# Create your models here.
class Seccion(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)
    apellido = models.CharField(max_length=200)
    cuit = models.CharField(max_length= 12,null= True, blank=True)
    seccion = models.CharField(null= False, blank=False, max_length=3,primary_key=True)
    e_mail = models.EmailField(blank=True, null= True)
    e_mail_agip = models.EmailField(blank=False)
    foto_user = models.ImageField(null=True, blank=True)
    direccion = models.CharField(max_length=150)
    telefono = models.CharField(max_length=150)

    def __str__(self):
        return str(self.seccion)
    class Meta:
        ordering= ('seccion',)

class Adjudicacion(models.Model):
    cuit = models.CharField(max_length=13, null= False, blank=False)
    apellido_nombre	= models.CharField (max_length=200, null=True, blank=True)
    adjudicacion = models.CharField (null= False, blank=False, max_length=30, primary_key=True)
    solicitud =	models.CharField (max_length=45, null= True, blank=True)
    nro_inscripto =	models.CharField (max_length=45, null= True, blank=True)
    dominio = models.CharField (max_length=20, null= True, blank=True)
    desc_adj = models.CharField (max_length=45, null= True, blank=True)
    cod_imp =  models.CharField (choices= impuestos ,max_length=15, null= True, blank=True)
    seccion = models.ForeignKey(Seccion, null=True, on_delete=models.SET_NULL)
    mandatario = models.CharField(max_length=100, null= True, blank=True)
    juzgado = models.CharField (choices= juzgados, null= True, blank=True, max_length=10)
    oficio = models.CharField (max_length=45, null=True, blank=True)  
    secretaria = models.CharField (choices= secretarias, null= True, blank=True, max_length=2)
    estado_juicio = models.CharField (max_length=45, null= True, blank=True)
    f_inicio_juic =	models.DateField (null= True, blank=True)
    fecha_adj =	models.DateField (null= True, blank=True)
    tipo_adm = models.CharField (max_length=45, null= True, blank=True)
    exp_adm	= models.CharField (max_length=45, null= True, blank=True)
    año_adm	= models.CharField (max_length = 10, null= True, blank=True)
    nro_exp = models.CharField (max_length=45, null= True, blank=True)
    año_exped =	models.CharField (max_length=10, null= True, blank=True)
    imp_nominal	= models.DecimalField(max_digits=20, decimal_places=2,null= True, blank=True)
    calle =	models.CharField (max_length=200, null= True, blank=True)
    puerta = models.CharField (max_length=45, null= True, blank=True)
    piso = models.CharField (max_length=45, null= True, blank=True)
    dpto = models.CharField (max_length=45, null= True, blank=True)
    oficina = models.CharField (max_length=45, null= True, blank=True)
    localidad = models.CharField (max_length=45, null= True, blank=True)
    cod_post = models.CharField (max_length=45, null= True, blank=True)
    const_deuda=models.FileField(upload_to='expedientes_git/constancias/',blank=True, null=True)
    date_created= models.DateTimeField(auto_now_add=True, null=True)
    

    def __str__(self):
        #return (self.apellido_nombre)
        return str(self.adjudicacion)
    class Meta:
        ordering= ['-f_inicio_juic','adjudicacion','-imp_nominal']

class Embargos(models.Model):
    seccion = models.ForeignKey(Seccion, on_delete=PROTECT)
    adjudicacion = models.OneToOneField(Adjudicacion, max_length=45,on_delete=PROTECT, blank=False, null=False)
    tipo_de_embargo = models.CharField (choices = tipo_de_embargo,default='preventivo', max_length=45, blank=False, null=False)
    clase_embargo = models.CharField (choices= clase_embargo, default="SOJ",max_length=45, null= True, blank=True)
    monto_embargado = models.DecimalField(max_digits=12, decimal_places=2,null= False, blank=False)
    estado = models.CharField (choices = estado_embargo, default="Trabado", max_length=45, null= True, blank=True)
    fecha_pedido_git = models.DateField(verbose_name="Fecha pedido de Embargo",blank=True, null=True)
    fecha_acreditacion= models.DateField(blank=True, null=True)
    fecha_pedido_levantamiento= models.DateField(verbose_name="Fecha pedido de Levantamiento",blank=True, null=True)
    orden_levantamiento = models.CharField (choices= orden_de_levantamiento, default='no',max_length=45, null=True, blank=True)
    fecha_levantamiento_git = models.DateField(blank=True, null=True)
    oficio_embargo= FileField(upload_to='embargos/oficios/',blank=True, null=True)
    oficio_lev_embargo = FileField(upload_to='embargos/ofic_levantamiento',blank=True, null=True)
    dia_ingreso_embargo= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.adjudicacion)

    class Meta:
        ordering = ('-fecha_pedido_git',) 

class Planes_de_pago(models.Model):
    seccion = models.ForeignKey(Seccion, null=True, on_delete=models.SET_NULL)
    adjudicacion = models.OneToOneField(Adjudicacion, max_length=45,on_delete=PROTECT, blank=False, null=False)
    imp_actualizado = models.DecimalField (max_digits=12,decimal_places=2, null= False, blank=False)
    fecha_de_suscripcion = models.DateField(blank=False, null=False)
    modalidad_de_pago = models.CharField (max_length=45, choices = mod_pago,default='Contado', null=True, blank=True) 
    cantidad_de_cuotas_plan = models.CharField (max_length=2, choices=cuotas, default='1', null=True, blank=True)
    honorarios_mandatario = models.DecimalField (max_digits=10,decimal_places=4, default='22212.81',null= True, blank=True)
    honorarios_procuracion = models.DecimalField (max_digits=10,decimal_places=4, default='7867.58',null= True, blank=True)
    fecha_de_pago_honorarios = models.DateField(blank= True, null= True)
    cuotas_de_honorarios = models.CharField (null= True, blank= True,choices= cuotas_hono, default= '1',max_length=2)
    acredito_comprobante = models.CharField(max_length=2, choices= comprobante, default='no',blank=True, null=True)
    estado_del_plan = models.CharField(max_length = 20, choices= estado_plan, default='Pendiente',blank=True, null=True)
    fecha_de_cancelacion = models.DateField(null=True, blank=True)
    email = models.EmailField(blank=True, null=True)
    telefono = models.CharField (max_length= 15,null = True, blank= True)
    celular = models.CharField (max_length= 15,null = True, blank = True)
    archivo_plan= models.FileField(upload_to='planes/planes_de_pago/', blank=True, null=True)
    comprobantes = models.FileField(upload_to='planes/comprobantes/', blank=True, null=True)
    dia_ingreso_plan= models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return str(self.adjudicacion)
    
    class Meta:
        ordering = ('-fecha_de_suscripcion',)


class Comprobantes_de_Pago(models.Model):
    adjudicacion = models.ForeignKey(Adjudicacion, null=True, blank=True, on_delete=models.PROTECT)
    comprobantes = models.FileField(upload_to='planes/comprobantes/', blank=True, null=True)
    dia_ingreso_comprobante= models.DateTimeField(auto_now_add=True, null=True, blank=True)


class Cbu_Contribuyente(models.Model):
    seccion = models.CharField(max_length= 3, null= True, blank=True)
    cuit= models.CharField(null= False, blank= False,max_length=15)
    impuesto = models.CharField(max_length=3, blank= True, null= True)
    adjudicacion= models.ForeignKey(Adjudicacion,on_delete=models.PROTECT, blank=True, null=True)
    cbu = models.CharField(max_length=30,blank=False, null=False)
    banco = models.CharField(max_length=200, blank=False, null=False)

    def __str__(self):
        #return (self.apellido_nombre)
        return str(self.cuit)
    class Meta:
        ordering= ['banco','cuit','impuesto']