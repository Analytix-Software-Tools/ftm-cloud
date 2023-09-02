from ftmcloud.core.service import Service
from ftmcloud.models.domains.industries.industry import Industry


class IndustriesService(Service):

    def __init__(self):
        super(IndustriesService, self).__init__(collection=Industry)
