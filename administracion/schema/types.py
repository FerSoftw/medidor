# graphene
import graphene
from graphene_django import DjangoObjectType
# modelos
from administracion.models import Operador
from administracion.models import Medidor
from administracion.models import HistorialConsumo

class OperadorType(DjangoObjectType):
    class Meta:
        model = Operador
        exclude_fields = ('password', )


class MedidorType(DjangoObjectType):
    class Meta:
        model=Medidor

class TotalMedidoresAndMedidores(graphene.ObjectType):
    total = graphene.Int()
    medidores = graphene.List(MedidorType)

class HistorialConsumoType(DjangoObjectType):
    class Meta:
        model=HistorialConsumo

class HistorialPorDiaType(graphene.ObjectType):
    medidor = graphene.Field(MedidorType, required=True)
    fecha = graphene.Date(required=True)
    consumo = graphene.Float(required=True)

class InfoConsumoMes(graphene.ObjectType):
    consumos_por_dia=graphene.List(HistorialPorDiaType, required=True)
    consumo_total_mes=graphene.Float(required=True)