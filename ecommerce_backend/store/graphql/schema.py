import graphene
from graphene_django import DjangoObjectType
from store.models import Product

class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ("id","name","slug","price","currency")

class Query(graphene.ObjectType):
    product = graphene.Field(ProductType, id=graphene.UUID(required=True))
    all_products = graphene.List(ProductType, first=graphene.Int(), skip=graphene.Int())

    def resolve_product(root, info, id):
        return Product.objects.get(id=id)

    def resolve_all_products(root, info, first=None, skip=None):
        qs = Product.objects.all()
        if skip:
            qs = qs[skip:]
        if first:
            qs = qs[:first]
        return qs

schema = graphene.Schema(query=Query)
