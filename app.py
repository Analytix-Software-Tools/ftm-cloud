from fastapi import FastAPI, Depends

from auth.jwt_bearer import token_listener
from config.config import initiate_database
from domains.users.controllers.controller import router as user_router
from domains.organizations.controllers.controller import router as organization_router
from domains.privileges.controllers.controller import router as privilege_router
from domains.industries.controllers.controller import router as industry_router
from domains.categories.controllers.controller import categories_router
from domains.attributes.controllers.controller import router as attribute_router
from domains.product_types.controllers.controller import product_type_router
from domains.products.controllers.controller import product_router
from domains.reports.controllers.controller import router as reports_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute


def custom_generate_unique_id(route: APIRoute):
    return f"{route.name}"


app = FastAPI(
    title="FTMCloud",
    description="Search engine and analytics API.",
    version="1.0.0",
    generate_unique_id_function=custom_generate_unique_id
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=['X-Total-Count']
)


@app.on_event("startup")
async def start_database():
    await initiate_database()


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "."}


app.include_router(organization_router, tags=['Organizations'], prefix='/api/v0/organizations',
                   dependencies=[Depends(token_listener)])
app.include_router(user_router, tags=["Users"], prefix="/api/v0/users")
app.include_router(privilege_router, tags=['Privileges'], prefix='/api/v0/privileges',
                   dependencies=[Depends(token_listener)])
app.include_router(industry_router, tags=['Industries'], prefix='/api/v0/industries',
                   dependencies=[Depends(token_listener)])
app.include_router(categories_router, tags=['Categories'], prefix='/api/v0/categories',
                   dependencies=[Depends(token_listener)])
app.include_router(attribute_router, tags=['Attributes'], prefix='/api/v0/attributes',
                   dependencies=[Depends(token_listener)])
app.include_router(product_type_router, tags=['Product Types'], prefix='/api/v0/product_types',
                   dependencies=[Depends(token_listener)])
app.include_router(product_router, tags=['Products'], prefix='/api/v0/products',
                   dependencies=[Depends(token_listener)])
app.include_router(reports_router, tags=['Reports'], prefix='/api/v0/search',
                   dependencies=[Depends(token_listener)])
