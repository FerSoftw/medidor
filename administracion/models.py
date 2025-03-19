import imp
from django.db import models
from sistemamedicion.constantes import *

# Create your models here.

class Operador(models.Model):
    VALID_ROL = [
        (ROL_ADMIN,"Administrador"),
        (ROL_OPERADOR, "Operador")
    ]
    nombres=models.CharField(max_length=100)
    apellidos=models.CharField(max_length=100)
    ci=models.CharField(max_length=8)
    u_name=models.CharField(max_length=30,unique=True)
    password=models.TextField()
    rol = models.CharField(max_length=3,choices=VALID_ROL, default=ROL_OPERADOR)

    def __str__(self) -> str:
        return self.nombres

class Medidor(models.Model):
    propietario=models.CharField(max_length=100)
    ci=models.CharField(max_length=8)
    direccion=models.CharField(max_length=100)
    sim=models.IntegerField(unique=True)
    numero=models.CharField(max_length=10,unique=True)
    estado=models.BooleanField(default=True)
    token_activo=models.TextField(null=True)
    token_nuevo=models.TextField(null=True)

    def __str__(self) -> str:
        return self.propietario

class HistorialConsumo(models.Model):
    medidor=models.ForeignKey(Medidor,on_delete=models.PROTECT, related_name="historial_consumo")
    consumo=models.FloatField()
    fecha=models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.medidor.propietario