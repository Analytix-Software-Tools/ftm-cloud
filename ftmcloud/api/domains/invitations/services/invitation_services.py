from ftmcloud.core.service import Service
from ftmcloud.models.invitation import Invitation
from ftmcloud.models.user import User
from ftmcloud.core.exception.exception import FtmException
from datetime import datetime, timedelta


class InvitationsService(Service):

    def __init__(self):
        super(InvitationsService, self).__init__(collection=Invitation)

    async def add_document(self, new_document: Invitation):
        user_exists = await User.find_one({"email": new_document.email})
        if user_exists is not None:
            raise FtmException('error.user.InvalidEmail')
        latest_timedelta = (datetime.now() - timedelta(hours=2))
        invitation_exists = await self.collection.find_one({"email": new_document.email,
                                                            "createdAt": {"$gte": latest_timedelta}})
        if invitation_exists is not None:
            raise FtmException('error.invitation.InvitationExists')
        await super(InvitationsService, self).add_document(new_document=new_document)
