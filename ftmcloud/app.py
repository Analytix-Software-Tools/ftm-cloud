from fastapi import Depends

from ftmcloud.cross_cutting.auth.jwt_bearer import token_listener
from ftmcloud.cross_cutting.db.db import initiate_database
from ftmcloud.core.app.app import FTMApi
from ftmcloud.api.rest.controllers.users.controllers.controller import router as user_router
from ftmcloud.api.rest.controllers.user_contacts.controllers.controller import router as user_contact_router
from ftmcloud.api.rest.controllers.organizations.controllers.controller import router as organization_router
from ftmcloud.api.rest.controllers.privileges.controllers.controller import router as privilege_router
from ftmcloud.api.rest.controllers.industries.controllers.controller import router as industry_router
from ftmcloud.api.rest.controllers.invitations.controllers.controller import router as invitation_router
from ftmcloud.api.rest.controllers.categories.controllers.controller import categories_router
from ftmcloud.api.rest.controllers.attributes.controllers.controller import router as attribute_router
from ftmcloud.api.rest.controllers.ftm_tasks.controllers.controller import ftm_tasks_router as ftm_task_router
from ftmcloud.api.rest.controllers.product_types.controllers.controller import product_type_router
from ftmcloud.api.rest.controllers.products.controllers.controller import product_router
from ftmcloud.api.rest.controllers.reports.controllers.controller import router as reports_router
from ftmcloud.api.rest.controllers.search.controllers.controller import router as search_router
from ftmcloud.api.rest.controllers.data_sources.controllers.controller import router as data_sources_router
from ftmcloud.cross_cutting.session.session import init_privilege_name_to_pid, init_default_organization

app = FTMApi()


@app.on_event("startup")
async def start_database():
    await initiate_database()
    await init_privilege_name_to_pid()
    await init_default_organization()


app.include_router(organization_router, tags=['Organizations'], prefix='/api/v0/organizations',
                   dependencies=[Depends(token_listener)])
app.include_router(user_router, tags=["Users"], prefix='/api/v0/users')
app.include_router(user_contact_router, tags=["UserContacts"], prefix='/api/v0/user_contacts',
                   dependencies=[Depends(token_listener)])
app.include_router(privilege_router, tags=['Privileges'], prefix='/api/v0/privileges',
                   dependencies=[Depends(token_listener)])
app.include_router(ftm_task_router, tags=['FtmTasks'], prefix='/api/v0/ftm_tasks',
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
app.include_router(data_sources_router, tags=['DataSources'], prefix='/api/v0/data_sources',
                   dependencies=[Depends(token_listener)])
