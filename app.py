from fastapi import FastAPI, Depends

from auth.jwt_bearer import JWTBearer
from config.config import initiate_database
from domains.users.controllers.controller import router as user_router
from domains.organizations.controllers.controller import router as organization_router
from domains.galleries.controllers.controller import router as gallery_router
from domains.student import router as student_router

app = FastAPI()

token_listener = JWTBearer()


@app.on_event("startup")
async def start_database():
    await initiate_database()


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "."}

app.include_router(organization_router, tags=['Organizations'], prefix='/api/v0/organizations',
                   dependencies=[Depends(token_listener)])
app.include_router(user_router, tags=["Users"], prefix="/api/v0/users")
app.include_router(student_router, tags=["Students"], prefix="/api/v0/student", dependencies=[Depends(token_listener)])
app.include_router(gallery_router, tags=['Galleries'], prefix='/api/v0/galleries',
                   dependencies=[Depends(token_listener)])
