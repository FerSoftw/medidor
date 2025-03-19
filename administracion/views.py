# HttpResponse
from django.http import HttpResponse
from administracion.sesiones import Manager
from administracion.models import HistorialConsumo
import json

# Create your views here.

def registrar_consumo(request):
    token = request.GET.get('token')
    consumo = request.GET.get('consumo')
    if token is None or consumo is None:
        return HttpResponse("Parametros invalidos", status=400)
    consumo = float(consumo)
    valido, medidor = Manager.validarTokenMedidor(token)
    if valido:
        # crear el historial de consumo
        historial = HistorialConsumo()
        historial.medidor = medidor
        historial.consumo = consumo
        historial.save()
        response_data = {}
        response_data['estado'] = medidor.estado
        response_data['token_nuevo'] = medidor.token_nuevo
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        return HttpResponse("No autorizado", status=401)
