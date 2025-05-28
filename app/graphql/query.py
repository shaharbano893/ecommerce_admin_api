import strawberry
from typing import Optional
from app.database.database import get_session
from app.models.models import Products
from app.schemas.graphql import ProductType, CreateProductInput


@strawberry.type
class Query:
    @strawberry.field
    def get_product(self, product_id: int) -> Optional[ProductType]:
        session = next(get_session())
        product = session.get(Products, product_id)
        return product

@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_product(self, create_product: CreateProductInput) -> ProductType:
        session = next(get_session())
        product = Products(**create_product.__dict__)
        session.add(product)
        session.commit()
        session.refresh(product)
        return ProductType(**product.model_dump())


graphql_schema = strawberry.Schema(query=Query, mutation=Mutation)