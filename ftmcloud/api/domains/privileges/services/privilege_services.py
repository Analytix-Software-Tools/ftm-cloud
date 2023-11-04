from ftmcloud.common.service.service import Service
from ftmcloud.models.domains.privilege import Privilege


class PrivilegesService(Service):

    def __init__(self):
        super(PrivilegesService, self).__init__(collection=Privilege)
