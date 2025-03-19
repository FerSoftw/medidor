import graphene
import administracion.schema.queries
import administracion.schema.mutations

class Query(administracion.schema.queries.Query, graphene.ObjectType):
    pass

class Mutation(administracion.schema.mutations.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)