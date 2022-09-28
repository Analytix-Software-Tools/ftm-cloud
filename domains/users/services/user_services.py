from fastapi import HTTPException

from crosscutting.service import Service
from models.user import User, UserProfile

user_collection = User


class UserService(Service):

    def __init__(self):
        super(UserService, self).__init__(collection=User)

    
    async def patch_users_profile(self, pid, patch_document_list):
        """Patches the user's own profile with information provided by them.
        """

        await self.validate_exists(pid=pid)
        for document in patch_document_list:
            if document.path == '/organizationPid' or document.path == '/privilegePid':
                raise HTTPException(status_code=422, detail="Invalid patch")

        return await self.patch(pid=pid, patch_document_list=patch_document_list)

    async def users_profile(self, pid) -> UserProfile:
        """Retrieves the user's full profile information by returning
        their profile, the organization they are in as well as the role.

        :param pid: The pid to find the profile for.
        :return: The user's profile.
        """
        user = await self.collection.find({"pid": pid}).aggregate([{
            "$lookup":
                {
                    "from": "organizations",
                    "localField": "organizationPid",
                    "foreignField": "pid",
                    "as": "organization"
                }
        }, {
            "$lookup":
                {
                    "from": "privileges",
                    "localField": "privilegePid",
                    "foreignField": "pid",
                    "as": "privilege"
                }
        }, {
            "$addFields": {
                "privilege": {"$arrayElemAt": ["$privilege", 0]},
                "organization": {"$arrayElemAt": ["$organization", 0]},
            }
        }, {
            "$project": {
                # "_id": 0,
                # "privilege._id": 0,
                "privilege.__v": 0,
                # "organization._id": 0
            }
        }]).to_list()
        if len(user) == 0:
            raise HTTPException(status_code=404, detail="User not found.")
        return user[0]
