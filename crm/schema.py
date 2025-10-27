import graphene

class UpdatedProductType(graphene.ObjectType):
    name = graphene.String()
    stock = graphene.Int()

class UpdateLowStockProducts(graphene.Mutation):
    class Arguments:
        pass

    success = graphene.Boolean()
    updated_products = graphene.List(UpdatedProductType)

    @staticmethod
    def mutate(root, info):
        updated = []
        try:
            from crm.models import Product
            low = Product.objects.filter(stock__lt=10)
            for p in low:
                p.stock = (p.stock or 0) + 10
                p.save(update_fields=["stock"])
                updated.append({"name": p.name, "stock": p.stock})
            return UpdateLowStockProducts(success=True, updated_products=updated)
        except Exception:
            return UpdateLowStockProducts(success=False, updated_products=[])

class Query(graphene.ObjectType):
    hello = graphene.String(description="Simple health check field")
    def resolve_hello(self, info):
        return "world"

class Mutation(graphene.ObjectType):
    update_low_stock_products = UpdateLowStockProducts.Field(name="updateLowStockProducts")

schema = graphene.Schema(query=Query, mutation=Mutation)
