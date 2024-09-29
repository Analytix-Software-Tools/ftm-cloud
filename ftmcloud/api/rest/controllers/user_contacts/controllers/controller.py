from fastapi import Body, APIRouter
from pydantic.validators import List

from ftmcloud.cross_cutting.auth.jwt_bearer import get_user_token, get_current_user, token_listener
from ftmcloud.core.exception.exception import default_exception_list
from ftmcloud.cross_cutting.models.patchdocument import PatchDocument
from ftmcloud.cross_cutting.models.response import Response, ResponseWithHttpInfo
from ftmcloud.domains.users.models.models import UserResponse, UserContact
from ftmcloud.domains.users.services.user_services import UserContactService
from ftmcloud.cross_cutting.views.views import controller
from ftmcloud.core.config.config import Settings

router = APIRouter()


@controller(router)
class UserContactsController:
    settings = Settings()

    @router.patch("/{pid}", response_model=Response, response_description="Successfully patched UserContact.",
                  responses=default_exception_list)
    async def patch_user_contact(self, pid: str, patch_list: List[PatchDocument] = Body(...)):
        """ Patches user contact.

        :param pid:
        :param patch_list:
        :return:
        """
        user_contact_service = UserContactService()
        await user_contact_service.patch(pid=pid, patch_document_list=patch_list)
        return Response(status_code=204, response_type='success', description="UserContact patched successfully.")

    @router.get("/", response_description="UserContacts retrieved", response_model=Response[UserContact],
                responses=default_exception_list)
    async def get_user_contacts(self, q: str | None = None, limit: int | None = None, offset: int | None = None,
                                sort: str | None = None, includeTotals: bool | None = None):
        """ Retrieves all user contacts.

        :param q:
        :param limit:
        :param offset:
        :param sort:
        :param includeTotals:
        :return:
        """
        user_contact_services = UserContactService()
        users = await user_contact_services.get_all(q=q, limit=limit, offset=offset, sort=sort)
        headers = {}
        if includeTotals is not None:
            headers = {"X-Total-Count": str(await user_contact_services.total(q=q))}
        return ResponseWithHttpInfo(status_code=200,
                                    response_type='success',
                                    model=UserContact,
                                    description="UserContacts retrieved successfully.",
                                    data=users,
                                    headers=headers)

    @router.delete("/{pid}", response_description="UserContact successfully deleted.", response_model=Response,
                   responses=default_exception_list)
    async def delete_user_contact(self, pid: str):
        """ Deletes user contact.

        :param pid:
        :return:
        """
        user_contact_services = UserContactService()
        await user_contact_services.delete_document(pid=pid)
        return Response(status_code=200, response_type="success", description="UserContact deleted.")
