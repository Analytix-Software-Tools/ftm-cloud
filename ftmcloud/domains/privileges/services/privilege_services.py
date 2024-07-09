from ftmcloud.cross_cutting.service.service import Service
from ftmcloud.domains.privileges.models.models import Privilege


class PrivilegesService(Service):

    def __init__(self):
        super(PrivilegesService, self).__init__(collection=Privilege)
