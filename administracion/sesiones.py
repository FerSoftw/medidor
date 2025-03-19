# native sesion imports
import jwt
#django hashers
from django.contrib.auth.hashers import check_password
#model admin import
from .models import Operador, Medidor
#other funcions import
from uuid import uuid4
import datetime
from sistemamedicion.constantes import *
#django timezone
from django.utils import timezone
# settings
from django.conf import settings

class Manager:
    secretNative=settings.SECRET_KEY

    @classmethod
    def generateToken(cls, operador, permanent):
        sessionid=uuid4()
        payload={
            'sessionid':str(sessionid),
            'operdid':operador.id
        }
        if not permanent:
            payload['exp'] = timezone.localtime() + datetime.timedelta(hours=1)
        encoded=jwt.encode(payload, cls.secretNative, algorithm='HS256')
        return encoded.decode("utf-8")

    @classmethod
    def iniciar(cls, u_name, password, permanent):
        if Operador.objects.filter(u_name=u_name).exists():
            operd=Operador.objects.get(u_name=u_name)
            if check_password(password, operd.password):
                token=Manager.generateToken(operd,permanent)
                return True, token, operd
            else:
                return False, "", None
        else:
            return False, "", None

    @classmethod
    def validar(cls, request):
        if 'Authorization' in request.headers:
            token=request.headers['Authorization']
            token=token[7:len(token)]
            try:
                payload=jwt.decode(token,cls.secretNative, algorithm='HS256')      
                admin=Operador.objects.get(id=payload['operdid'])
                return True, admin
            except:
                return False, None
        else:
            return False, None
        
    @classmethod
    def generateTokenMedidor(cls, medidor):
        sessionid=uuid4()
        payload={
            'sessionid':str(sessionid),
            'medidor':medidor.id
        }
        encoded=jwt.encode(payload, cls.secretNative, algorithm='HS256')
        return encoded.decode("utf-8")
    
    @classmethod
    def validarTokenMedidor(cls, token):
        try:
            payload=jwt.decode(token, cls.secretNative, algorithm='HS256')
            medidor=Medidor.objects.get(id=payload['medidor'])
            if medidor.token_nuevo == token:
                medidor.token_activo = token
                medidor.token_nuevo = None
                medidor.save()
            if medidor.token_activo == token:
                return True, medidor
            else:
                return False, None
        except:
            return False, None