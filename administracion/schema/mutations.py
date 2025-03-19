# import graphene
import graphene
# types
from .types import *
# models
from administracion.models import *
# hasher
from django.contrib.auth.hashers import make_password
# constantes
from sistemamedicion.constantes import *
# sesiones
from administracion.sesiones import Manager
# settings
from django.conf import settings

# Mutaciones de operador
class CreateOperador(graphene.Mutation):
    estado = graphene.Boolean()
    error = graphene.String()
    operador = graphene.Field(OperadorType)

    class Arguments:
        nombres=graphene.String(required = True)
        apellidos=graphene.String(required = True)
        ci=graphene.String(required = True)
        u_name=graphene.String(required = True)
        password=graphene.String(required = True)
        rol=graphene.String(required = True)

    def mutate(self, info, **input):
        valid, actual_operd = Manager.validar(info.context)
        if valid or settings.INSTALL_MODE:
            try:
                nombres=input.get("nombres")
                apellidos=input.get("apellidos")
                ci=input.get("ci")
                u_name=input.get("u_name")
                password=input.get("password")
                rol=input.get("rol")
                # cifrar password
                pass_cifrada=make_password(password)
                if rol not in [ROL_ADMIN, ROL_OPERADOR]:
                    return CreateOperador(estado=False, error="El rol no es válido")
                new_operador=Operador(nombres=nombres, apellidos=apellidos, ci=ci, u_name=u_name, password=pass_cifrada, rol=rol)
                new_operador.save()
                return CreateOperador(estado=True, operador=new_operador)
            except Exception as e:
                return CreateOperador(estado = False, error = str(e))
        else:
            return CreateOperador(estado = False, error = "Sesión invalida")

class UpdateOperador(graphene.Mutation):
    estado = graphene.Boolean()
    error = graphene.String()
    operador = graphene.Field(OperadorType)

    class Arguments:
        id = graphene.ID(required = True)
        nombres=graphene.String(required = True)
        apellidos=graphene.String(required = True)
        ci=graphene.String(required = True)
        u_name=graphene.String(required = True)
        password=graphene.String()
        rol=graphene.String(required = True)
    
    def mutate(self, info, **input):
        id = input.get("id")
        nombres=input.get("nombres")
        apellidos=input.get("apellidos")
        ci=input.get("ci")
        u_name=input.get("u_name")
        password=input.get("password")
        rol=input.get("rol")
        if rol not in [ROL_ADMIN,ROL_OPERADOR]:
            return CreateOperador(estado = False, error = "Rol invalido")
        # recuperar en la base de datos 
        operd = Operador.objects.get(id=id)
        operd.nombres = nombres
        operd.apellidos = apellidos
        operd.u_name = u_name
        operd.ci = ci
        if password is not None:
            operd.password = make_password(password)
        operd.rol = rol
        operd.save()   
        return UpdateOperador(estado = True, operador = operd) 

class DeleteOperador(graphene.Mutation):
    estado = graphene.Boolean()
    error = graphene.String()

    class Arguments:
        id = graphene.ID(required = True)
        
    def mutate(self, info, **input):
        id = input.get("id")
        # eliminar en la base de datos
        operd = Operador.objects.get(id=id)
        operd.delete()
        return DeleteOperador(estado = True)

class Login(graphene.Mutation):
    estado = graphene.Boolean()
    error = graphene.String()
    token = graphene.String()

    class Arguments:
        u_name = graphene.String(required=True)
        password=graphene.String(required=True)
        permanent=graphene.Boolean(required=True)

    def mutate(self, info, **input):
        try:
            u_name=input.get('u_name')
            password=input.get('password')
            permanent=input.get('permanent')
            valid, token, operd = Manager.iniciar(u_name, password, permanent)
            if valid:
                return Login(estado=valid, token=token)
            else:
                return Login(estado=False, error="Datos inválidos")
        except Exception as e:
            return Login(estado=False, error=str(e))

# Mutaciones de medidor
class CreateMedidor(graphene.Mutation):
    estado = graphene.Boolean()
    error = graphene.String()
    medidor = graphene.Field(MedidorType)

    class Arguments:
        propietario=graphene.String(required = True)
        ci=graphene.String(required = True)
        direccion=graphene.String(required = True)
        sim=graphene.Int(required = True)
        numero=graphene.String(required = True)

    def mutate(self, info, **input):
        valid, actual_operd = Manager.validar(info.context)
        if valid:
            try:
                propietario=input.get("propietario")
                ci=input.get("ci")
                direccion=input.get("direccion")
                sim=input.get("sim")
                numero=input.get("numero")
                new_medidor=Medidor(propietario=propietario, ci=ci, direccion=direccion, sim=sim, numero=numero)
                new_medidor.save()
                # generar token
                token_activo = Manager.generateTokenMedidor(new_medidor)
                new_medidor.token_activo = token_activo
                new_medidor.save()
                return CreateMedidor(estado=True, medidor=new_medidor)
            except Exception as e:
                return CreateMedidor(estado = False, error = str(e))
        else:
            return CreateMedidor(estado = False, error = "Sesión invalida")

class UpdateMedidor(graphene.Mutation):
    estado = graphene.Boolean()
    error = graphene.String()
    medidor = graphene.Field(MedidorType)

    class Arguments:
        id = graphene.ID(required = True)
        propietario=graphene.String(required = True)
        ci=graphene.String(required = True)
        direccion=graphene.String(required = True)
        sim=graphene.Int(required = True)
        numero=graphene.String(required = True)

    def mutate(self, info, **input):
        valid, actual_operd = Manager.validar(info.context)
        if valid:
            try:
                id = input.get("id")
                propietario=input.get("propietario")
                ci=input.get("ci")
                direccion=input.get("direccion")
                sim=input.get("sim")
                numero=input.get("numero")
                # recuperar en la base de datos 
                medidor = Medidor.objects.get(id=id)
                medidor.propietario = propietario
                medidor.ci = ci
                medidor.direccion = direccion
                medidor.sim = sim
                medidor.numero = numero
                medidor.save()   
                return UpdateMedidor(estado = True, medidor = medidor) 
            except Exception as e:
                return UpdateMedidor(estado = False, error = str(e))
        else:
            return UpdateMedidor(estado = False, error = "Sesión invalida")

class DeleteMedidor(graphene.Mutation):
    estado = graphene.Boolean()
    error = graphene.String()

    class Arguments:
        id = graphene.ID(required = True)
        
    def mutate(self, info, **input):
        valid, actual_operd = Manager.validar(info.context)
        if valid:
            try:
                id = input.get("id")
                # eliminar en la base de datos
                medidor = Medidor.objects.get(id=id)
                medidor.delete()
                return DeleteMedidor(estado = True)
            except Exception as e:
                return DeleteMedidor(estado = False, error = str(e))
        else:
            return DeleteMedidor(estado = False, error = "Sesión invalida")

class StatusMedidor(graphene.Mutation):
    estado = graphene.Boolean()
    error = graphene.String()
    medidor = graphene.Field(MedidorType)

    class Arguments:
        id = graphene.ID(required = True)
        estado = graphene.Boolean(required = True)
        
    def mutate(self, info, **input):
        valid, actual_operd = Manager.validar(info.context)
        if valid:
            try:
                id = input.get("id")
                estado = input.get("estado")
                # recuperar en la base de datos 
                medidor = Medidor.objects.get(id=id)
                medidor.estado = estado
                medidor.save()   
                return StatusMedidor(estado = True, medidor = medidor) 
            except Exception as e:
                return StatusMedidor(estado = False, error = str(e))
        else:
            return StatusMedidor(estado = False, error = "Sesión invalida")

class TokenNuevo(graphene.Mutation):
    estado = graphene.Boolean()
    error = graphene.String()
    medidor = graphene.Field(MedidorType)

    class Arguments:
        id = graphene.ID(required = True)
        
    def mutate(self, info, **input):
        valid, actual_operd = Manager.validar(info.context)
        if valid:
            try:
                id = input.get("id")
                # recuperar en la base de datos 
                medidor = Medidor.objects.get(id=id)
                # generar token
                token_nuevo = Manager.generateTokenMedidor(medidor)
                medidor.token_nuevo = token_nuevo
                medidor.save()
                return TokenNuevo(estado = True, medidor = medidor) 
            except Exception as e:
                return TokenNuevo(estado = False, error = str(e))
        else:
            return TokenNuevo(estado = False, error = "Sesión invalida")

# Mutaciones generales
class Mutation:
    # Mutaciones de operador
    create_operador = CreateOperador.Field()
    update_operador = UpdateOperador.Field()
    delete_operador = DeleteOperador.Field()
    login = Login.Field()

    # Mutaciones de medidor
    create_medidor = CreateMedidor.Field()
    update_medidor = UpdateMedidor.Field()
    delete_medidor = DeleteMedidor.Field()
    status_medidor = StatusMedidor.Field()
    token_nuevo = TokenNuevo.Field()