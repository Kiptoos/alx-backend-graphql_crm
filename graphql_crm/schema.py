import graphene
from crm.schema import Query as CRMQuery, Mutation as CRMMutation


class Query(CRMQuery, graphene.ObjectType):
    """
    Root query type.
    Inherits all CRM queries and adds a simple 'hello' field.
    """

    hello = graphene.String(description="Simple test field")

    def resolve_hello(root, info):
        return "Hello, GraphQL!"


class Mutation(CRMMutation, graphene.ObjectType):
    """
    Root mutation type.
    Inherits all CRM mutations.
    """

    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
