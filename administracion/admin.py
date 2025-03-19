from django.contrib import admin
from .models import Operador
from .models import Medidor

# Register your models here.
admin.site.register(Operador)
admin.site.register(Medidor)