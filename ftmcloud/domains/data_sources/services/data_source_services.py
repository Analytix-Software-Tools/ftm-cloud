from ftmcloud.cross_cutting.service.service import Service
from ftmcloud.domains.data_sources.models.models import DataSource
from ftmcloud.domains.users.models.models import User


class DataSourcesService(Service):

    def __init__(self):
        super(DataSourcesService, self).__init__(collection=DataSource)
        