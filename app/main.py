from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
from app.database.database import create_db_and_tables
from app.routers import products, sales, inventory
from app.graphql.query import graphql_schema



app = FastAPI(
    title="E-commerce Admin API",
    description="API for managing e-commerce products, sales, and inventory",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

graphql_router = GraphQLRouter(graphql_schema)
# Include routers
app.include_router(products.router)
app.include_router(sales.router)
app.include_router(inventory.router)

app.include_router(graphql_router, prefix="/graphql")

@app.get("/")
async def root():
    return {
        "message": "Welcome to E-commerce Admin API",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }
