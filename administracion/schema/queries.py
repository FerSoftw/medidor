# graphene imports
import graphene
# models
from administracion.models import *
# types
from .types import *
from django.db.models import Q
from django.db.models import Max
from django.db.models.functions import TruncDate
import datetime
# sesiones
from administracion.sesiones import Manager



class Query(graphene.ObjectType):

    # Operadores
    operador = graphene.Field(OperadorType, id=graphene.ID(required=True))
    all_operador = graphene.List(OperadorType)
    actual_operador = graphene.Field(OperadorType)

    def resolve_operador(self, info, **input):
        valid, actual_operd = Manager.validar(info.context)
        if valid:
            id = input.get("id")
            return Operador.objects.get(id=id)
        else:
            return None

    def resolve_all_operador(self, info, **input):
        valid, actual_operd = Manager.validar(info.context)
        if valid:
            return Operador.objects.all().order_by('apellidos', 'nombres')
        else:
            return []

    def resolve_actual_operador(self, info, **input):
        valid, actual_operd = Manager.validar(info.context)
        return actual_operd

    # Medidores
    medidor = graphene.Field(MedidorType, id=graphene.ID(required=True))
    all_medidores = graphene.Field(TotalMedidoresAndMedidores, termino=graphene.String(), pagina=graphene.Int(required=True))
    total_medidores = graphene.Int()

    def resolve_medidor(self, info, **input):
        valid, actual_operd = Manager.validar(info.context)
        if valid:
            id = input.get("id")
            return Medidor.objects.get(id=id)
        else:
            return None

    def resolve_all_medidores(self, info, termino=None, pagina=1):
        valid, actual_operd = Manager.validar(info.context)
        if valid:
            NUM_RESULTS = 4
            inicio = (pagina - 1) * NUM_RESULTS
            fin = inicio + NUM_RESULTS
            medidores = []
            if termino is None or termino == "":
                medidores = Medidor.objects.all()[inicio:fin]
            else:
                medidores = Medidor.objects.filter(Q(sim__icontains=termino) | Q(numero__icontains=termino))[inicio:fin]
            total_medidores = Medidor.objects.count() if (termino is None or termino =="") else Medidor.objects.filter(Q(sim__icontains=termino) | Q(numero__icontains=termino)).count()
            return TotalMedidoresAndMedidores(total=total_medidores, medidores=medidores)
        else:
            return TotalMedidoresAndMedidores(total=0, medidores=[])
    
    def resolve_total_medidores(self, info):
        valid, actual_operd = Manager.validar(info.context)
        if valid:
            return Medidor.objects.all().count()
        else:
            return 0 

    # HistorialConsumo
    historial_mes = graphene.Field(InfoConsumoMes, medidor_id=graphene.ID(required=True), year=graphene.Int(), month=graphene.Int())

    def resolve_historial_mes(self, info, medidor_id, year=None, month=None):
        valid, actual_operd = Manager.validar(info.context)
        if valid:
            lista_ultimos_consumos_subquery = HistorialConsumo.objects.filter(medidor_id=medidor_id,  fecha__year=year, fecha__month=month).annotate(dia=TruncDate('fecha')).values('dia').annotate(ultimo_registro=Max('fecha')).values('ultimo_registro')
            lista_ultimos_consumos = HistorialConsumo.objects.filter(medidor_id=medidor_id).filter(fecha__in=lista_ultimos_consumos_subquery)
            limite_inferior=datetime.datetime(year=year, month=month, day=1, hour=0, minute=0)
            consumo_anterior = HistorialConsumo.objects.filter(fecha__lt=limite_inferior).order_by('-fecha').first()
            resultado=[]
            ultimo_consumo=0 if consumo_anterior==None else consumo_anterior.consumo
            consumo_total_mes=0
            for consumo_dia in lista_ultimos_consumos:
                consumo = consumo_dia.consumo - ultimo_consumo
                resultado.append(
                    HistorialPorDiaType(
                        medidor=consumo_dia.medidor,
                        fecha=consumo_dia.fecha.date(),
                        consumo=consumo
                    )
                )
                consumo_total_mes+=consumo
                ultimo_consumo=consumo
            return InfoConsumoMes(consumos_por_dia=resultado, consumo_total_mes=consumo_total_mes)
        else:
            return []