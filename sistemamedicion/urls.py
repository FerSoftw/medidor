"""sistemamedicion URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from graphene_file_upload.django import FileUploadGraphQLView
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.conf.urls.static import static
from .schema import schema
from administracion.views import registrar_consumo

urlpatterns = [
    path('admin/', admin.site.urls),
    path('schema/', csrf_exempt(FileUploadGraphQLView.as_view(schema=schema, graphiql=settings.DEBUG))),
    path('registrar_consumo/', registrar_consumo)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
