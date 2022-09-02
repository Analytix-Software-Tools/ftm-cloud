from crosscutting.service import Service
from models.organization import Organization


class OrganizationsService(Service):

    def __init__(self):
        super(OrganizationsService, self).__init__(collection=Organization)
