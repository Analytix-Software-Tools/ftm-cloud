from ftmcloud.cross_cutting.service.service import Service
from ftmcloud.domains.industries.models.models import Industry


class IndustriesService(Service):

    def __init__(self):
        super(IndustriesService, self).__init__(collection=Industry)
