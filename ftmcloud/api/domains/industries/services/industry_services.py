from ftmcloud.common.service.service import Service
from ftmcloud.models.domains.industry import Industry


class IndustriesService(Service):

    def __init__(self):
        super(IndustriesService, self).__init__(collection=Industry)
