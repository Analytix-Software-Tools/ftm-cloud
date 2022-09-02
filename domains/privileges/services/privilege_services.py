from crosscutting.service import Service
from models.privilege import Privilege


class PrivilegesService(Service):

    def __init__(self):
        super(PrivilegesService, self).__init__(collection=Privilege)
