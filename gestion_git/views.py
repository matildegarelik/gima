from django.shortcuts import render
from distutils.command.upload import upload
from re import template
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect,HttpResponse, JsonResponse, request
from django.views import View
from django.views.generic import TemplateView
from os import read
import os
from django.forms.forms import Form
from tablib import Dataset
from django.core import serializers
import json
from .utils import leer_patentes
from django.conf import settings
# FORMULARIOS
from .forms import Formulario_embargo, Formulario_expedientes_Git, Formulario_planes, Crear_Expediente_Git_Form, Crear_Mandatario_Form, Crear_Formulario_User, Formulario_comprobantes

# MODELOS
from .models import Cbu_Contribuyente, Comprobantes_de_Pago, Seccion,Adjudicacion,Planes_de_pago,Embargos, UserSeccion, Patente

# Filtros
from.filters import Expediente_Git_Filtro, Embargos_Git_Filtro, Planes_Git_Filtro,Cbu_contribuyente_Filtro, Patente_Filtro

# PAGINADOR
from django.core.paginator import Paginator

# SUBIR ARCHIVOS
from django.core.files.storage import FileSystemStorage

#Registro de usuario
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

# Login
from django.contrib.auth import authenticate, login,logout

#decoradores para bloquear accesos sin registro
from django.contrib.auth.decorators import login_required

#Decoradores
from .decorators import *

#Importar Grupos para delimitar vistas
from django.contrib.auth.models import Group

# Emails
from django.core.mail import send_mail, EmailMessage
from django.conf import settings

# Resources
from .admin import Planes_Resource, Embargos_Resource, Adjudicacion_Resource

# Create your views here.

#Pagina de Registro

@usuarios_habilitados(roles_permitidos=['admin'])
def pagina_de_registro(request):
    
    form = Crear_Formulario_User()
    secciones = Seccion.objects.all()
    
    if request.method == 'POST':
        form= Crear_Formulario_User(request.POST)
        if form.is_valid():
            user= form.save()
            username = form.cleaned_data.get('username')
            
            group= Group.objects.get(name=request.POST['grupo'])
            user.groups.add(group)

            sec =  UserSeccion.objects.create(
                id=UserSeccion.objects.all().count()+1,
                seccion=Seccion.objects.get(seccion=request.POST['seccion']),
                user=user
            )
            sec.save()

            messages.success(request, 'La cuenta fue creada con éxito para ' + username)
            
            return redirect('/gestion_git/login/')
    context={'form':form,'secciones':secciones}
    return render(request, 'gestion_git/accounts/register.html', context)

#LOGIN
def pagina_de_login(request):

    if request.method =='POST':
        username= request.POST.get('username')
        password= request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if(Group.objects.get(name='admin') in user.groups.all()):
                return redirect('git:secciones')
            elif(Group.objects.get(name='contador') in user.groups.all()):
                sec = UserSeccion.objects.get(user=user)
                return redirect('git:planes_sec',sec.seccion)   
            elif(Group.objects.get(name='auxiliar') in user.groups.all()):
                sec = UserSeccion.objects.get(user=user)
                return redirect('git:seccion', sec.seccion)
            elif(Group.objects.get(name='abogado') in user.groups.all()):
                sec = UserSeccion.objects.get(user=user)
                return redirect('git:seccion', sec.seccion)
            else: 
                return HttpResponse(user.groups.all())
        else:
            messages.info(request,'El nombre de ususario o la contraseña ingresados es incorrecto')
    context={}
    return render (request, 'gestion_git/login.html', context)

#LOGOUT
def pagina_de_logout(request):
    logout(request)
    return redirect ('login' )

# Pagina de Usuario

@usuarios_habilitados(roles_permitidos=['auxiliar', 'admin','abogado'])

def pagina_usuario(request):
    if(not hasattr(request.user,'seccion') or request.user.seccion==None):
        seccion= UserSeccion.objects.get(user=request.user.id)
        request.user.seccion=Seccion.objects.get(seccion=seccion.seccion)
    lista_datos = Seccion.objects.get(seccion=request.user.seccion)
    expedientes = Adjudicacion.objects.filter(seccion_id=request.user.seccion)
    embargos = Embargos.objects.filter(adjudicacion__seccion_id=request.user.seccion)
    planes = Planes_de_pago.objects.filter(adjudicacion__seccion_id=request.user.seccion) 
    
    filtro_exped_git= Expediente_Git_Filtro(request.GET, queryset=expedientes)
    expedientes = filtro_exped_git.qs

    filtro_exped_embargo = Embargos_Git_Filtro(request.GET, queryset=embargos)
    embargos = filtro_exped_embargo.qs

    filtro_exped_plan = Planes_Git_Filtro(request.GET, queryset=planes)
    planes = filtro_exped_plan.qs

    
    contar_expe = expedientes.count()
    contar_embargos= embargos.count()
    contar_planes = planes.count()

    # Paginador de hojas
    p = Paginator(expedientes, 25)
    page = request.GET.get('page')
    expedientes = p.get_page(page)
    print('paginas:',expedientes)

    context={'expedientes':expedientes,
    'lista_datos':lista_datos,
    'embargos':embargos, 'planes':planes,
    'contar_expe':contar_expe,
    'embargos': embargos,
    'contar_embargos':contar_embargos,
    'contar_planes':contar_planes,
    'filtro_exped_git':filtro_exped_git,
    'filtro_exped_embargo':filtro_exped_embargo,
    'filtro_exped_plan':filtro_exped_plan
    }

    return render (request, 'gestion_git/accounts/users.html', context)


# HOME del SITIO

def Home(request):
    return render(request, 'login.html')

# Ingreso al sitio
@solo_admin
def base(request):
    return render(request, 'base.html')

# CREAR SECCION
@usuarios_habilitados(roles_permitidos=['admin'])
def crear_seccion(request):

    if request.method == 'POST':
        crear_seccion_form = Crear_Mandatario_Form(request.POST)
        if crear_seccion_form.is_valid():
            crear_seccion_form.save()
            return redirect('git:secciones')
    else:
        crear_seccion_form = Crear_Mandatario_Form()

    return render(request,'gestion_git/crear_seccion.html', 
    {'crear_seccion_form':crear_seccion_form}
    )  

# Secciones: Mandatarios
@usuarios_habilitados(roles_permitidos=['admin','auxiliar'])
@solo_admin
def secciones_git(request):
    secciones = Seccion.objects.all()

    return render (request, 'gestion_git/secciones.html', 
    {'secciones':secciones
    }
    )

#seccion individual
@usuarios_habilitados(roles_permitidos=['auxiliar','admin','abogado'])

def seccion_manda(request, pk_seccion):
    seccion = Seccion.objects.get(seccion=pk_seccion)
    
    #expedientes = seccion.adjudicacion_set.all()
    expedientes = Adjudicacion.objects.filter(seccion_id=pk_seccion)
    embargos_manda = Embargos.objects.filter(adjudicacion__seccion_id=pk_seccion)
    planes_manda = Planes_de_pago.objects.filter(adjudicacion__seccion_id=pk_seccion) 

    if(request.GET.get('ordenar')):
        expedientes= expedientes.order_by(request.GET.get('ordenar'))
  
    filtro_exped_git= Expediente_Git_Filtro(request.GET, queryset=expedientes)
    expedientes = filtro_exped_git.qs

    filtro_exped_embargo = Embargos_Git_Filtro(request.GET, queryset=embargos_manda)
    embargos_manda = filtro_exped_embargo.qs
    filtro_exped_plan = Planes_Git_Filtro(request.GET, queryset=planes_manda)
    planes_manda = filtro_exped_plan.qs


    contar_expe = expedientes.count()
    contar_embargos= embargos_manda.count()
    contar_planes = planes_manda.count()

    # Paginador de hojas
    p = Paginator(expedientes, 25)
    page = request.GET.get('page')
    expedientes = p.get_page(page)
    print('paginas:',expedientes)
    

    context= {'seccion':seccion,
    'expedientes':expedientes,
    'contar_expe':contar_expe,
    'embargos_manda': embargos_manda,
    'contar_embargos':contar_embargos,
    'contar_planes':contar_planes,
    'filtro_exped_git':filtro_exped_git,
    'filtro_exped_embargo':filtro_exped_embargo, 
    'filtro_exped_plan':filtro_exped_plan,
    'ordenar':request.GET.get('ordenar')
    }
    return render(request, 'gestion_git/seccion.html',
    context 
    )

# Crear Expediente GIT
@usuarios_habilitados(roles_permitidos=['admin'])

def crear_expediente_git_seccion(request,pk):
    seccion_expediente = Seccion.objects.get(seccion=pk)
    
    crear_expediente_form= Crear_Expediente_Git_Form(instance=seccion_expediente, initial={'seccion_expediente':seccion_expediente})
    
    if request.method == 'POST':
        crear_expediente_form = Crear_Expediente_Git_Form(request.POST, request.FILES)
        if crear_expediente_form.is_valid():
            crear_expediente_form.save()
            return redirect('home')
    
    return render (request,'gestion_git/crear_expediente.html',
    {'crear_expediente_form':crear_expediente_form,}
    )

# Importar Expediente GIT

def importar_expediente_git(request):
    if request.method == 'POST':
        file_format = request.POST['file-format']
        expe_git = Adjudicacion_Resource()
        dataset = Dataset()
        nuevos_expe_git = request.FILES['importData']

        if file_format == 'CSV':
            imported_data = dataset.load(nuevos_expe_git.read().decode('utf-8'),format='csv')
            result = expe_git.import_data(dataset, dry_run=True)
        elif file_format == 'JSON':
            imported_data = dataset.load(nuevos_expe_git.read().decode('utf-8'),format='json')
            result = expe_git.import_data(dataset, dry_run=True)
            
        if not result.has_errors():
            expe_git.import_data(dataset, dry_run=False)

    return render(request, 'gestion_git/importar_expe_git.html') 

# Ver Expediente GIT Individual
@usuarios_habilitados(roles_permitidos=['auxiliar','admin','abogado'])

def ver_expediente_git(request,pk):
    expediente_git = Adjudicacion.objects.get(adjudicacion=pk)
    planes = Planes_de_pago.objects.all()
    embargos= Embargos.objects.all()
    #cbu= Cbu_Contribuyente.objects.filter(adjudicacion_id=pk)
    cbus=Cbu_Contribuyente.objects.filter(cuit=expediente_git.cuit)
    cbu='-'
    if(cbus.count()):
        cbu=cbus.first()
    dom_exist = False
    if expediente_git.dominio and len(Patente.objects.filter(dominio=expediente_git.dominio))>0:
        dom_exist=True
        
    #filtro_cbu= Cbu_contribuyente_Filtro(request.GET, queryset=cbu)
    #cbu = filtro_cbu.qs
    
    context={'expediente_git':expediente_git,
    'planes':planes, 
    'embargos':embargos,
    'cbu':cbu,
    'dom_exist':dom_exist
    }
    return render(request,'gestion_git/expediente_git.html',context)
   

# Editar expediente GIT
@usuarios_habilitados(roles_permitidos=['mandatarios','admin'])

def editar_expediente_git(request,pk):
    adjudicaciones_git = Adjudicacion.objects.get(adjudicacion=pk)
   
    if request.method =='GET':
        crear_expediente_form = Crear_Expediente_Git_Form(instance=adjudicaciones_git)
    else:
        crear_expediente_form = Crear_Expediente_Git_Form(request. POST, request.FILES, instance= adjudicaciones_git)
        if crear_expediente_form.is_valid():
            crear_expediente_form.save()
            return redirect('git:expediente_git_global')

    return render(request, 'gestion_git/crear_expediente.html',
    {'crear_expediente_form':crear_expediente_form}
    )

# Listado Global Expedientes GIT
@usuarios_habilitados(roles_permitidos=['admin'])

def expedientes_git(request):
    expediente_git = Adjudicacion.objects.all()
    #print(len(expediente_git))

    embargos_git = Embargos.objects.all()
    embargo_trabado = embargos_git.filter(estado='trabado').count()
    embargo_levantado= embargos_git.filter(estado='levantado').count()
    planes_git= Planes_de_pago.objects.all()

    if(request.GET.get('ordenar')):
        expediente_git= expediente_git.order_by(request.GET.get('ordenar'))

    filtro_exped_git= Expediente_Git_Filtro(request.GET, queryset=expediente_git)
    expediente_git= filtro_exped_git.qs

    contar_expe = expediente_git.count()
    contar_embargos= embargos_git.count()
    contar_planes = planes_git.count()

    # Paginador de hojas
    p = Paginator(expediente_git, 25)
    page = request.GET.get('page')
    expediente_git = p.get_page(page)
    print('paginas:',expediente_git)

    context= {'expediente_git':expediente_git,
    'embargos_git': embargos_git, 
    'embargo_trabado':embargo_trabado,
    'embargo_levantado':embargo_levantado,
    'filtro_exped_git':filtro_exped_git,
    'expediente_git':expediente_git,
    'contar_expe':contar_expe,
    'contar_embargos':contar_embargos,
    'contar_planes':contar_planes,
    'ordenar':request.GET.get('ordenar')
    }

    return render(request, 'gestion_git/expediente_git_global.html', context
    )


# Exportar listado Global de expedientes
@usuarios_habilitados(roles_permitidos=['admin'])
def exportar_expedientes_git(request):
    if request.method == 'POST':
        file_format = request.POST['file-format']
        adjudicaciones_resource = Adjudicacion_Resource()
        dataset = adjudicaciones_resource.export()
        if file_format == 'CSV':
            response = HttpResponse(dataset.csv, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="exported_data.csv"'
            return response        
        elif file_format == 'JSON':
            response = HttpResponse(dataset.json, content_type='application/json')
            response['Content-Disposition'] = 'attachment; filename="exported_data.json"'
            return response
        elif file_format == 'XLS (Excel)':
            response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="exported_data.xls"'
            return response   

    return render(request, 'gestion_git/exportar_adjudiaciones.html')




# Listado GLobal Planes de Pagos
@usuarios_habilitados(roles_permitidos=['admin'])

def planes_de_pago(request):
    lista_planes = Planes_de_pago.objects.all()

    total_planes = lista_planes.count()
    planes_pendientes = lista_planes.filter(estado_del_plan='Pendiente').count()
    planes_nulos = lista_planes.filter(estado_del_plan='Nulo').count()
    planes_cancelados =lista_planes.filter(estado_del_plan='Cancelado').count()

    filtro_planes = Planes_Git_Filtro(request.GET, queryset=lista_planes)
    lista_planes= filtro_planes.qs

    if(request.GET.get('ordenar')):
        lista_planes= lista_planes.order_by(request.GET.get('ordenar'))
     
    # Paginador de hojas
    p = Paginator(lista_planes, 25)
    page = request.GET.get('page')
    lista_planes = p.get_page(page)
    print('paginas:',lista_planes)
    

    return render(request, 'gestion_git/planes.html',
    {'lista_planes':lista_planes,
    'planes_pendientes':planes_pendientes,
    'total_planes': total_planes,
    'planes_nulos': planes_nulos,
    'planes_cancelados':planes_cancelados,
    'filtro_planes':filtro_planes,
    'lista_planes':lista_planes,
    'ordenar':   request.GET.get('ordenar')    
    }
    )

# Crear plan de pagos desde la seccion
@usuarios_habilitados(roles_permitidos=['admin'])

def nuevo_plan(request, pk):
    seccion_git = Seccion.objects.get(seccion=pk)
    
    form_plan = Formulario_planes(instance= seccion_git, initial={'seccion_git':seccion_git})
    
    if request.method == 'POST':
        form_plan = Formulario_planes(request.POST, request.FILES)
        if form_plan.is_valid():
            form_plan.save()
            return redirect('users')

    return render (request, 'gestion_git/nuevo_plan.html',
    {'form_plan':form_plan}
    )

# Crear plan de pagos desde adjudicación
@usuarios_habilitados(roles_permitidos=['admin'])

def plan_adjudicacion(request,pk):
    adjudicaciones_git = Adjudicacion.objects.get(adjudicacion=pk)
    form_plan = Formulario_planes(instance=adjudicaciones_git, initial={'adjudicaciones_git':adjudicaciones_git})
    #plan = Planes_de_pago.objects.latest('id').delete()
    if request.method == 'POST':
        form_plan = Formulario_planes(data=request.POST, files=request.FILES)
        if form_plan.is_valid():
            form_plan.save()
            manda = Seccion.objects.get(seccion=request.POST.get('seccion'))
            embargo = Embargos.objects.filter(adjudicacion_id=request.POST.get('adjudicacion'))
            plan = Planes_de_pago.objects.latest('id')
            mensaje=f'''Se ha creado un plan de pago:
                -Importe actualizado: ${plan.imp_actualizado}
                -Modalidad de pago: {plan.modalidad_de_pago}
                -Fecha de suscripción: {plan.fecha_de_suscripcion}
                -Honorarios Mandatario: ${plan.honorarios_mandatario} 
                -Honorarios procuracion: ${plan.honorarios_procuracion}
                -Cuotas: {plan.cuotas_de_honorarios}

            Acceda al siguiente link para subir los comprobantes: http://gimaapp.herokuapp.com/gestion_git/comprobantes/?adjudicacion={request.POST.get('adjudicacion')}
            '''
            if len(embargo)>0:
                mensaje+=' y al siguiente link para seguir el estado del embargo: http://gimaapp.herokuapp.com/gestion_git/seg-embargo/'+str(embargo[0].id)
            email = EmailMessage(
                'Información plan de pago', 
                mensaje, 
                manda.e_mail_agip, [request.POST.get('email')]
            )
            if plan.archivo_plan:
                email.attach_file(os.path.join(settings.MEDIA_ROOT,str(plan.archivo_plan)))
            email.send()
            return redirect('git:planes')
        
    return render (request, 'gestion_git/nuevo_plan_adj.html',
    {'form_plan':form_plan,'adjudicacion':adjudicaciones_git}
    )

# Actualizar plan de pago
@usuarios_habilitados(roles_permitidos=['admin'])

def actualizar_plan(request, pk):
    planes = Planes_de_pago.objects.get(id=pk)
    form_plan = Formulario_planes(instance=planes)
    adj = Adjudicacion.objects.get(adjudicacion=planes.adjudicacion_id)

    if request.method == 'POST':
        form_plan = Formulario_planes(data= request.POST,files=request.FILES, instance= planes)
        if form_plan.is_valid():
            form_plan.save()
            #comprobante = request.FILES.get('comprobantes')
            #if(comprobante):
            #    Comprobantes_de_Pago.objects.create(comprobantes=comprobante,adjudicacion_id=request.POST['adjudicacion'])
            return redirect('git:users')

    return render(request, 'gestion_git/nuevo_plan.html',
    {'form_plan':form_plan, 'adjudicacion':adj} 
    )

# Eliminar plan de pago
@usuarios_habilitados(roles_permitidos=['mandatarios','admin'])

def eliminar_plan(request, pk):
    planes = Planes_de_pago.objects.get(id=pk)
    if request.method == 'POST':
        planes.delete()
        return redirect('git:users')
        
    context = {'planes':planes}
    return render(request, 'gestion_git/eliminar_plan.html', context)

# Ver Planes por Seccion
@usuarios_habilitados(roles_permitidos=['auxiliar','admin','contador','abogado'])

def ver_planes(request, pk):
    lista_datos = Seccion.objects.get(seccion=pk)

    datos_causa = Adjudicacion.objects.filter(seccion_id=pk)
    datos_embargo = Embargos.objects.filter(adjudicacion__seccion_id=pk)
    planes_seccion = Planes_de_pago.objects.filter(adjudicacion__seccion_id=pk)

    if(request.GET.get('ordenar')):
        planes_seccion= planes_seccion.order_by(request.GET.get('ordenar'))
    
    total_planes = planes_seccion.count()
    planes_pendientes = planes_seccion.filter(estado_del_plan='Pendiente').count()
    planes_nulos = planes_seccion.filter(estado_del_plan='Nulo').count()
    planes_cancelados = planes_seccion.filter(estado_del_plan='Cancelado').count()

    filtro_planes = Planes_Git_Filtro(request.GET, queryset=planes_seccion)
    planes_seccion= filtro_planes.qs

    # Paginador de hojas
    p = Paginator(planes_seccion, 25)
    page = request.GET.get('page')
    planes_seccion = p.get_page(page)
    print('paginas:',planes_seccion)

    
    context= {'lista_datos':lista_datos,
    'datos_causa':datos_causa,
    'datos_embargo': datos_embargo,
    'planes_seccion':planes_seccion,
    'total_planes':total_planes, 
    'planes_pendientes':planes_pendientes,
    'planes_nulos':planes_nulos, 
    'planes_cancelados':planes_cancelados,
    'filtro_planes':filtro_planes,
    'ordenar':request.GET.get('ordenar')
    }

    return render (request, 'gestion_git/planes_seccion.html',context    )

# Vista comprobantes de pago

class MainView(TemplateView):
    template_name= 'subir_comprobantes.html'

#Subir archivos múltiples
@usuarios_habilitados(roles_permitidos=['auxiliar','admin','abogado'])
def subir_comprobantes(request):
    if request.method== "POST":
        comprobante = request.FILES.get('file')
        Comprobantes_de_Pago.objects.create(comprobantes=comprobante,adjudicacion_id=request.POST['adjudicacion'])
        return HttpResponse('')
    return JsonResponse ({'post'})

#Listado Global Embargos
@usuarios_habilitados(roles_permitidos=['admin'])

def embargos(request):
    lista_embargos = Embargos.objects.all()
    
    total_embargos = lista_embargos.count()
    embargos_soj = lista_embargos.filter(clase_embargo= 'SOJ').count()
    embargo_trabado = lista_embargos.filter(estado='Trabado').count()
    embargo_levantado= lista_embargos.filter(estado='Levantado').count()

    if(request.GET.get('ordenar')):
        lista_embargos= lista_embargos.order_by(request.GET.get('ordenar'))

    filtro_embargos= Embargos_Git_Filtro(request.GET, queryset=lista_embargos)
    lista_embargos= filtro_embargos.qs

    # Paginador de hojas
    p = Paginator(lista_embargos, 25)
    page = request.GET.get('page')
    lista_embargos = p.get_page(page)
    print('paginas:',lista_embargos)
     
    context = {'lista_embargos':lista_embargos, 'total_embargos':total_embargos,
    'embargos_soj': embargos_soj,'embargo_trabado':embargo_trabado, 
    'embargo_levantado':embargo_levantado, 'filtro_embargos':filtro_embargos,'ordenar':request.GET.get('ordenar')}

    return render (request, 'gestion_git/embargos.html',context
    )

# Listado Embargos por Seccion
@usuarios_habilitados(roles_permitidos=['auxiliar','admin','abogado'])

def ver_embargo(request, pk):
    lista_datos = Seccion.objects.get(seccion=pk)

    datos_causa = Adjudicacion.objects.filter(seccion_id=pk)
    embargos_seccion = Embargos.objects.filter(adjudicacion__seccion_id=pk)
    datos_plan = Planes_de_pago.objects.filter(adjudicacion__seccion_id=pk)

    if(request.GET.get('ordenar')):
        embargos_seccion= embargos_seccion.order_by(request.GET.get('ordenar'))
    
    total_embargos = embargos_seccion.count()
    embargos_soj = embargos_seccion.filter(clase_embargo='soj').count()
    embargo_trabado = embargos_seccion.filter(estado='Trabado').count()
    embargo_levantado= embargos_seccion.filter(estado='Levantado').count()

    filtro_exped_git= Expediente_Git_Filtro(request.GET, queryset=datos_causa)
    datos_causa = filtro_exped_git.qs
    
    filtro_exped_embargo = Embargos_Git_Filtro(request.GET, queryset=embargos_seccion)
    embargos_seccion = filtro_exped_embargo.qs

    # Paginador de hojas
    p = Paginator(embargos_seccion, 25)
    page = request.GET.get('page')
    embargos_seccion = p.get_page(page)
    print('paginas:',embargos_seccion)

    context = {'lista_datos':lista_datos,'datos_causa':datos_causa,'datos_plan':datos_plan,
    'embargos_seccion':embargos_seccion,'total_embargos':total_embargos, 'embargos_soj':embargos_soj,
    'embargo_trabado':embargo_trabado,'embargo_levantado':embargo_levantado,
    'filtro_exped_embargo':filtro_exped_embargo,'filtro_exped_git':filtro_exped_git, 'ordenar':request.GET.get('ordenar')
    }
    return render (request, 'gestion_git/embargos_seccion.html',context
    )

# Embargo desde Seccion
@usuarios_habilitados(roles_permitidos=['auxiliar','admin'])

#def nuevo_embargo(request, pk):
#    seccion_git  = Seccion.objects.get(seccion=pk)
#    form_embargo = Formulario_embargo(instance= seccion_git, initial={'seccion_git':seccion_git})
#    adjudicaciones = Adjudicacion.objects.filter(seccion_id=seccion_git.seccion)
#    if request.method == 'POST': 
#        form_embargo = Formulario_embargo(data=request.POST, files=request.FILES)
#        if form_embargo.is_valid():
#            form_embargo.save()
#            return redirect('git:users')
#     
#    return render (request, 'gestion_git/nuevo_embargo.html', 
#    {'form_embargo':form_embargo, 'seccion':seccion_git,'adjudicaciones':adjudicaciones}
#    )

# Embargo desde Adjudicación
@usuarios_habilitados(roles_permitidos=['auxiliar','admin','abogado'])

def embargo_adjudicacion(request,pk):
    adjudicaciones_git  = Adjudicacion.objects.get(adjudicacion=pk)
    
    form_embargo = Formulario_embargo(instance=adjudicaciones_git, initial={'adjudicaciones_git':adjudicaciones_git})

    if request.method == 'POST':
        form_embargo= Formulario_embargo(request.POST, request.FILES)

        if form_embargo.is_valid():
            form_embargo.save()
            return redirect('git:users')
  
    return render (request, 'gestion_git/nuevo_embargo.html',
    {'form_embargo':form_embargo,'seccion':adjudicaciones_git.seccion_id,'adjudicacion':adjudicaciones_git}
    )

# Actualizar Embargo
@usuarios_habilitados(roles_permitidos=['auxiliar','admin','abogado'])

def actualizar_embargo(request,pk):
    embargos = Embargos.objects.get(id=pk)
    form_embargo = Formulario_embargo(instance= embargos)

    if request.method == 'POST': 
        form_embargo = Formulario_embargo(data=request.POST, files= request.FILES, instance=embargos)
        if form_embargo.is_valid():
            form_embargo.save()
            return redirect('git:users')

    return render (request, 'gestion_git/nuevo_embargo.html', 
    {'form_embargo':form_embargo}
    )

#Eliminar Emabrgo
@usuarios_habilitados(roles_permitidos=['admin'])

def eliminar_embargo(request, pk):
    embargos = Embargos.objects.get(id=pk)
    if request.method == 'POST':
        embargos.delete()
        return redirect('git:users')


    context = {'embargos':embargos}
    return render(request, 'gestion_git/eliminar_embargo.html', context)

@usuarios_habilitados(roles_permitidos=['auxiliar','admin','contador','abogado'])
def exportar_planes(request):
    if request.method == 'POST':
        file_format = request.POST['file-format']
        planes_resource = Planes_Resource()
        
        filterdata=Planes_de_pago.objects.all()
        # Chequear filtros: seccion, adjudicacion, estado, desde y hasta
        if request.GET['seccion']:
            filterdata= filterdata.filter(adjudicacion__seccion_id=request.GET['seccion'])
        if request.GET['adj']:
            filterdata= filterdata.filter(adjudicacion_id=request.GET['adj'])
        if request.GET['estado']:
            filterdata= filterdata.filter(estado_del_plan=request.GET['estado'])
        if request.GET['desde']:
            filterdata= filterdata.filter(fecha_de_suscripcion__gte=request.GET['desde'])
        if request.GET['hasta']:
            filterdata= filterdata.filter(fecha_de_suscripcion__lte=request.GET['hasta'])
        

        dataset = planes_resource.export(filterdata)
        if file_format == 'CSV':
            response = HttpResponse(dataset.csv, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="exported_data.csv"'
            return response        
        elif file_format == 'JSON':
            response = HttpResponse(dataset.json, content_type='application/json')
            response['Content-Disposition'] = 'attachment; filename="exported_data.json"'
            return response
        elif file_format == 'XLS (Excel)':
            response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="exported_data.xls"'
            return response   

    return render(request, 'gestion_git/exportar_planes.html')
    
@usuarios_habilitados(roles_permitidos=['admin'])
def importar_planes(request):
    if request.method == 'POST':
        file_format = request.POST['file-format']
        planes_resource = Planes_Resource()
        dataset = Dataset()
        nuevos_planes = request.FILES['importData']

        if file_format == 'CSV':
            imported_data = dataset.load(nuevos_planes.read().decode('utf-8'),format='csv')
            result = planes_resource.import_data(dataset, dry_run=True)
        elif file_format == 'JSON':
            imported_data = dataset.load(nuevos_planes.read().decode('utf-8'),format='json')
            result = planes_resource.import_data(dataset, dry_run=True)
            
        if not result.has_errors():
            planes_resource.import_data(dataset, dry_run=False)

    return render(request, 'gestion_git/importar_planes.html')  


@usuarios_habilitados(roles_permitidos=['auxiliar','admin','abogado'])
def exportar_embargos(request):
    if request.method == 'POST':

        filterdata=Embargos.objects.all()
        # Chequear filtros: seccion, adjudicacion, estado, desde y hasta
        if request.GET['seccion']:
            filterdata= filterdata.filter(adjudicacion__seccion_id=request.GET['seccion'])
        if request.GET['estado']:
            filterdata= filterdata.filter(estado=request.GET['estado'])
        if request.GET['clase']:
            filterdata= filterdata.filter(clase_embargo=request.GET['clase'])
        if request.GET['desde']:
            filterdata= filterdata.filter(fecha_pedido_git__gte=request.GET['desde'])
        if request.GET['hasta']:
            filterdata= filterdata.filter(fecha_pedido_git__lte=request.GET['hasta'])

        file_format = request.POST['file-format']
        planes_resource = Embargos_Resource()
        dataset = planes_resource.export(filterdata)
        if file_format == 'CSV':
            response = HttpResponse(dataset.csv, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="exported_data.csv"'
            return response        
        elif file_format == 'JSON':
            response = HttpResponse(dataset.json, content_type='application/json')
            response['Content-Disposition'] = 'attachment; filename="exported_data.json"'
            return response
        elif file_format == 'XLS (Excel)':
            response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="exported_data.xls"'
            return response   

    return render(request, 'gestion_git/exportar_embargos.html')

@usuarios_habilitados(roles_permitidos=['auxiliar','admin','abogado'])
def cbu_contribuyente(request):
    cbu = Cbu_Contribuyente.objects.all()

    filtro_cbu = Cbu_contribuyente_Filtro(request.GET, queryset=cbu)
    cbu = filtro_cbu.qs

    # Paginador de hojas
    p = Paginator(cbu, 20)
    page = request.GET.get('page')
    cbu = p.get_page(page)
    print('paginas:',cbu)

    context= {'cbu':cbu, 'filtro_cbu':filtro_cbu}

    return render(request, 'gestion_git/cbu_contribuyentes.html',context)
    
def get_comprobantes(request,pk):
    comprobantes = Comprobantes_de_Pago.objects.filter(adjudicacion_id=pk)
    for c in comprobantes:
        c.comprobantes = c.comprobantes.url
    comp_json=serializers.serialize('json',comprobantes)
    return JsonResponse(comp_json,safe=False)

def cambiar_estado_plan(request):
    pk = request.GET.get('pk')
    estado = request.GET.get('estado')
    if(pk and estado):
        plan = Planes_de_pago.objects.get(id=pk)
        plan.estado_del_plan=estado
        plan.save()
        return HttpResponse('success')
    return HttpResponse('error')

def cambiar_estado_embargo(request):
    pk = request.GET.get('pk')
    estado = request.GET.get('estado')
    if(pk and estado):
        embargo = Embargos.objects.get(id=pk)
        embargo.estado=estado
        embargo.save()
        return HttpResponse('success')
    return HttpResponse('error')

def cambiar_fact_plan(request):
    pk = request.GET.get('pk')
    facturado = request.GET.get('facturado')
    if(pk and facturado):
        plan = Planes_de_pago.objects.get(id=pk)
        plan.facturado= facturado=='1' 
        plan.save()
        return HttpResponse('success')
    return HttpResponse('error')

def subir_comprobantes_view(request):
    if request.method== "POST":
        comprobante = request.FILES.get('file')
        Comprobantes_de_Pago.objects.create(comprobantes=comprobante,adjudicacion_id=request.POST['adjudicacion'])
        return render(request, 'gestion_git/subir_comprobantes.html',{
            'submitted': True
        })
    if Adjudicacion.objects.filter(adjudicacion__exact=request.GET.get('adjudicacion')).exists():
        adj=Adjudicacion.objects.get(adjudicacion=request.GET.get('adjudicacion'))
        return render(request, 'gestion_git/subir_comprobantes.html',{
            'adjudicacion': adj
        })
    else:
        return render(request, 'gestion_git/subir_comprobantes.html',{
            'adjudicacion': False 
        })

def seg_embargo(request,pk):
    return render(request,'gestion_git/seg-embargo.html',{
        'embargo': Embargos.objects.get(id=pk)
    })

def subir_patentes(request):
    secciones = Seccion.objects.all()
    #Patente.objects.filter().delete()
    patentes = Patente.objects.all()
    filtro_patentes = Patente_Filtro(request.GET, queryset=patentes)
    patentes = filtro_patentes.qs
    

    # Paginador de hojas
    p = Paginator(patentes, 25)
    page = request.GET.get('page')
    patentes = p.get_page(page)
    print('paginas:',patentes)

    if request.method== "POST":
        archivo = request.FILES.get('file')
        if archivo != None:
            leer_patentes(archivo,request.POST.get('seccion'))
            messages.success(request, 'Patentes cargada con éxito')
        
    return render(request, 'gestion_git/subir_patentes.html',{
        'secciones':secciones,
        'patentes': patentes,
        'filtro_patentes':filtro_patentes
     })

def ver_patente(request,dominio):
    patentes = Patente.objects.filter(dominio=dominio)
    
    context={'patentes':patentes, 'dominio':dominio, 'seccion': patentes.first().seccion_id}
    return render(request,'gestion_git/detalle_patente.html',context)
 
    