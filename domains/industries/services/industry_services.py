from crosscutting.service import Service
from models.industry import Industry


class IndustriesService(Service):

    def __init__(self):
        super(IndustriesService, self).__init__(collection=Industry)
