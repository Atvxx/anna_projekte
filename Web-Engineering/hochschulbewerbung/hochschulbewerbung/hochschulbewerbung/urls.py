"""
URL configuration for hochschulbewerbung project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from bewerbung import views
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', lambda request: redirect('startseite')), # generiert mit Copilot
    path('admin/', admin.site.urls),
    path('bewerbung/', views.bewerbung_view, name='bewerbung'),
    path('danke/<str:code>/', views.danke_seite, name='danke'),
    path('', lambda request: redirect('bewerbung')),
    path('login/', views.benutzer_login, name='login'),
    path('logout/', views.benutzer_logout, name='logout'),
    path('api/bewerbung/', views.bewerbung_api, name='api-bewerbung'),
    path('api/kontakt/', views.kontakt_api, name='api-kontakt'),
    path('status/', views.status_check_view, name='status_check'),
    path('api/status/', views.status_check_api, name='api_status_check'),
    path('statuscode/', views.sende_statuscode, name='sende_statuscode'),
    path('startseite/', views.startseite, name='startseite'),
    path('kontakt/', views.kontakt, name='kontakt'),
    path('voraussetzungen/', views.voraussetzungen_view, name='voraussetzungen'),
    path('bewerbungsprozess/', views.bewerbungsprozess_view, name='bewerbungsprozess'),
    path('studiengaenge/', views.studiengaenge_view, name='studiengaenge'),
    path('bwl/', views.bwl_view, name='bwl'),
    path('psychologie/', views.psychologie_view, name='psychologie'),
    path('winfo/', views.winfo_view, name='winfo'),
    path('dbm/', views.dbm_view, name='dbm'),
    path('i18n/', include('django.conf.urls.i18n')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)