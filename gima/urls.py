from unicodedata import name
from django.contrib import admin
from django.urls import include, path, re_path
from gestion_git.views import pagina_de_login
from gestion_git.views import MainView, subir_comprobantes
from gestion_git import views
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('gestion_git/', include(('gestion_git.urls','git'))),
    path('', pagina_de_login, name='login'),
    path('gestion_git/accounts', include('django.contrib.auth.urls')),    
    path('__debug__/', include('debug_toolbar.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)