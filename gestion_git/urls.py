from django.contrib import admin
from django.urls import path
from gestion_git import views
from django.conf import settings
from django.contrib.auth import views as auth_views
from gestion_git.views import MainView



urlpatterns = [
    # BASE
    path('base', views.base, name='base'),

    # Registro y Login/out
    path('register', views.pagina_de_registro, name='register'),
    path('login/',views.pagina_de_login, name= 'login'),
    path('logout/',views.pagina_de_logout, name= 'logout'),

    # Usuarios
    path('users/', views.pagina_usuario, name='users'),
    
    # Mandatarios
    path('crear_seccion/',views.crear_seccion, name="crear_seccion"),
    path('secciones/', views.secciones_git, name='secciones'),
    path('seccion/<str:pk_seccion>/', views.seccion_manda, name='seccion'),
   

    # Expedientes
    path('crear_expediente_seccion/<str:pk>/',views.crear_expediente_git_seccion, name='crear_expediente_seccion'),
    path('expediente_git/<str:pk>/', views.ver_expediente_git, name="expediente_git"),
    path('editar_expediente_git/<str:pk>/', views.editar_expediente_git, name='editar_expediente_git'),
    path('expediente_git_global',views.expedientes_git, name="expediente_git_global"),
    path('exportar_adjudicaciones/',views.exportar_embargos, name="exportar_adjudicaciones"),
    path('importar_expe_git/',views.importar_expediente_git, name="importar_expe_git"),

    # Planes de Pago
    path('planes', views.planes_de_pago, name="planes"),
    path('nuevo_plan_adj/<str:pk>/',views.plan_adjudicacion, name="nuevo_plan_adj"),
    path('actualizar_plan/<str:pk>/',views.actualizar_plan, name='actualizar_plan'),
    path('eliminar_plan/<str:pk>/',views.eliminar_plan, name='eliminar_plan'),
    path('planes/<str:pk>/',views.ver_planes,name='planes_sec'),
    path('nuevo_plan_seccion/<str:pk>/',views.nuevo_plan, name="nuevo_plan_seccion"),
    path('exportar_planes/',views.exportar_planes, name="exportar_planes"),
    path('importar_planes/',views.importar_planes, name="importar_planes"),
    path('',views.MainView.as_view(), name='main-view'),
    path('subir_comprobantes/',views.subir_comprobantes, name='subir_comprobantes'),
     

    # Embargos
    path('embargos/',views.embargos,name="embargos"),
    path('embargos/<str:pk>/',views.ver_embargo,name='embargos_sec'),
    path('nuevo_embargo/<str:pk>/',views.nuevo_embargo, name="nuevo_embargo"),
    path('nuevo_embargo_adj/<str:pk>/',views.embargo_adjudicacion, name="nuevo_embargo_adj"),
    path('actualizar_embargo/<str:pk>/',views.actualizar_embargo, name='actualizar_embargo'),
    path('eliminar_embargo/<str:pk>/',views.eliminar_embargo, name='eliminar_embargo'),
    path('exportar_embargos/',views.exportar_embargos, name="exportar_embargos"),

    # CBU Contribuyentes
    path('cbu_contribuyentes/',views.cbu_contribuyente, name="cbu_contribuyentes"),
    

    # Recuperar Usuario y Password
    path('password_reset/',auth_views.PasswordResetView.as_view(template_name='gestion_git/accounts/password_reset.html'), name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='gestion_git/accounts/accountspassword_reset/done.html'),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='gestion_git/accounts/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done',auth_views.PasswordResetCompleteView.as_view(template_name='gestion_git/accounts/password_reset_done.html'), name='password_reset_complete'),
]