from fastapi import FastAPI, Body
from pydantic import BaseModel
from starlette.responses import JSONResponse

from ftmcloud.domains.users.services.user_services import UserService

"""
Service which notifies users by email and various other techniques.
"""

app = FastAPI()


class NotificationRequest(BaseModel):
    """
    Request model which represents the body of a notification request.
    """
    email: str


@app.post('/notify/:id')
async def notify_user_by_email(request: NotificationRequest = Body(...)):
    """ Notifies the specified user by email.

    :param request
    :return:
    """
    user_service = UserService()
    try:
        await user_service.notify_user(
            email=""
        )
    except Exception as e:
        return JSONResponse({"error": str(e)})
