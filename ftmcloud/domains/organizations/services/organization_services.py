from ftmcloud.cross_cutting.service.service import Service
from ftmcloud.domains.organizations.models.models import Organization


class OrganizationsService(Service):

    def __init__(self):
        super(OrganizationsService, self).__init__(collection=Organization)
