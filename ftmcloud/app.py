from fastapi import Depends

from ftmcloud.common.auth.jwt_bearer import token_listener
from ftmcloud.common.db.db import initiate_database
from ftmcloud.core.app.app import FTMApi
from ftmcloud.api.domains.users.controllers.controller import router as user_router
from ftmcloud.api.domains.organizations.controllers.controller import router as organization_router
from ftmcloud.api.domains.privileges.controllers.controller import router as privilege_router
from ftmcloud.api.domains.industries.controllers.controller import router as industry_router
from ftmcloud.api.domains.invitations.controllers.controller import router as invitation_router
from ftmcloud.api.domains.categories.controllers.controller import categories_router
from ftmcloud.api.domains.attributes.controllers.controller import router as attribute_router
from ftmcloud.api.domains.model_configurations.controllers.controller import router as model_configuration_router
from ftmcloud.api.domains.product_types.controllers.controller import product_type_router
from ftmcloud.api.domains.products.controllers.controller import product_router
from ftmcloud.api.domains.reports.controllers.controller import router as reports_router
from ftmcloud.api.domains.search.controllers.controller import router as search_router
from ftmcloud.api.domains.tasks.controllers.controller import router as task_router

app = FTMApi()


@app.on_event("startup")
async def start_database():
    await initiate_database()


app.include_router(organization_router, tags=['Organizations'], prefix='/api/v0/organizations',
                   dependencies=[Depends(token_listener)])
app.include_router(user_router, tags=["Users"], prefix='/api/v0/users')
app.include_router(privilege_router, tags=['Privileges'], prefix='/api/v0/privileges',
                   dependencies=[Depends(token_listener)])
app.include_router(industry_router, tags=['Industries'], prefix='/api/v0/industries',
                   dependencies=[Depends(token_listener)])
app.include_router(invitation_router, tags=['Invitations'], prefix='/api/v0/invitations',
                   dependencies=[Depends(token_listener)])
app.include_router(categories_router, tags=['Categories'], prefix='/api/v0/categories',
                   dependencies=[Depends(token_listener)])
app.include_router(attribute_router, tags=['Attributes'], prefix='/api/v0/attributes',
                   dependencies=[Depends(token_listener)])
app.include_router(product_type_router, tags=['Product Types'], prefix='/api/v0/product_types',
                   dependencies=[Depends(token_listener)])
app.include_router(product_router, tags=['Products'], prefix='/api/v0/products',
                   dependencies=[Depends(token_listener)])
app.include_router(reports_router, tags=['Reports'], prefix='/api/v0/reports',
                   dependencies=[Depends(token_listener)], deprecated=True)
app.include_router(search_router, tags=['Search'], prefix='/api/v0/search',
                   dependencies=[Depends(token_listener)])
app.include_router(model_configuration_router, tags=["Model Configurations"], prefix='/api/v0/model_configurations',
                   dependencies=[Depends(token_listener)])
app.include_router(task_router, tags=["Tasks"], prefix='/api/v0/tasks',
                   dependencies=[Depends(token_listener)])
