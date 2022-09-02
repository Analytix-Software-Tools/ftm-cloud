from crosscutting.service import Service
from models.gallery import Gallery


class GalleriesService(Service):

    def __init__(self):
        super(GalleriesService, self).__init__(collection=Gallery)
