import graphene
import artists.schema


class Query(artists.schema.Query, graphene.ObjectType):
    pass


class Mutation(artists.schema.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
