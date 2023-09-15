from datetime import datetime, timedelta

from fastapi import Body, APIRouter, Depends

from ftmcloud.core.auth.jwt_bearer import get_current_user
from ftmcloud.core.exception.exception import default_exception_list
from ftmcloud.api.domains.invitations.services.invitation_services import InvitationsService
from ftmcloud.models.domains.invitations.invitation import Invitation

from ftmcloud.models.response import Response, ResponseWithHttpInfo
from ftmcloud.models.domains.users.user import User
from ftmcloud.common.session.session import has_elevated_privileges
from ftmcloud.common.views.views import controller

router = APIRouter()


@controller(router)
class InvitationsController:
    current_user: User = Depends(get_current_user)

    @router.post("/", response_model=Invitation, response_description="Successfully registered invitation.",
                 responses=default_exception_list)
    async def add_invitation(self, new_invitation: Invitation = Body(...)):
        """Registers a new invitation within the space.
        """
        invitation_service = InvitationsService()
        new_invitation.organizationPid = self.current_user.organizationPid
        await invitation_service.add_document(new_invitation)
        return new_invitation

    @router.get("/", response_description="Invitations retrieved", response_model=Response[Invitation],
                responses=default_exception_list)
    async def get_invitations(self, q: str | None = None, limit: int | None = None, offset: int | None = None,
                             sort: str | None = None, includeTotals: bool | None = None):
        """Gets all invitations using the user defined parameters.
        """
        invitation_service = InvitationsService()
        latest_timedelta = (datetime.now() - timedelta(hours=2))
        additional_filters = {"createdAt": {"$gte": latest_timedelta}}
        if not has_elevated_privileges(self.current_user):
            additional_filters["organizationPid"] = self.current_user.organizationPid
        invitations = await invitation_service.get_all(q=q, limit=limit, offset=offset, sort=sort,
                                                       additional_filters=additional_filters)
        headers = {}
        if includeTotals is not None:
            headers = {"X-Total-Count": str(await invitation_service.total(q))}
        return ResponseWithHttpInfo(data=invitations,
                                    model=Invitation,
                                    description="Invitations retrieved successfully.",
                                    headers=headers)

    @router.delete("/{pid}", response_description="Invitation successfully deleted.", response_model=Response,
                   responses=default_exception_list)
    async def delete_invitation(self, pid: str):
        """Deletes a user.
        """
        invitation_service = InvitationsService()
        if not has_elevated_privileges(user=self.current_user):
            await invitation_service.validate_exists(pid=pid, additional_filters=
                                                     {"organizationPid": self.current_user.organizationPid})
        await invitation_service.delete_document(pid=pid)
        return Response(status_code=200, response_type="success", description="Invitation deleted.")
