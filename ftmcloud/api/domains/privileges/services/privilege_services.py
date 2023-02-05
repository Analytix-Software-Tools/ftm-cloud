from ftmcloud.core.service import Service
from ftmcloud.models.privilege import Privilege


class PrivilegesService(Service):

    def __init__(self):
        super(PrivilegesService, self).__init__(collection=Privilege)
