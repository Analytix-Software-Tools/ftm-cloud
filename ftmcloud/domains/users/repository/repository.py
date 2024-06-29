from ftmcloud.common.repository.repository import Repository
from ftmcloud.models.domains.user import User


class UsersRepository(Repository):
    
    def __init__(self):
        super().__init__(model_cls=User)
