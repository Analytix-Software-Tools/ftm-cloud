from ftmcloud.core.exception.exception import FtmException
from ftmcloud.cross_cutting.service.service import Service
from ftmcloud.domains.data_sources.models.models import DataSourceRepository
from ftmcloud.domains.industries.models.models import Industry
from ftmcloud.domains.organizations.models.models import Organization
from ftmcloud.domains.users.models.models import User


class OrganizationsService(Service):

    def __init__(self):
        self._data_source_repository = DataSourceRepository()
        super(OrganizationsService, self).__init__(collection=Organization)

    async def _validate_data_source_pid(self, pid):
        exists = await self._data_source_repository.find({"pid": pid}, first=True)
        if not exists:
            raise FtmException('error.data_source.NotFound')

    async def add_validator(self, new_document):
        if new_document.dataSourcePid:
            await self._validate_data_source_pid(pid=new_document.dataSourcePid)

    async def patch_document_validator(self, document, patch_document_list, current_user: User | None = None):
        for i in range(0, len(patch_document_list)):
            if patch_document_list[i].path == '/industryPids':
                patch_len = len(patch_document_list[i].value)
                for j in range(0, patch_len):
                    exists = await Industry.find_one(
                        {"pid": patch_document_list[i].value[j], "isDeleted": {"$ne": "true"}})
                    if exists is None:
                        raise FtmException('error.industry.NotFound')
            if patch_document_list[i].path == '/dataSourcePid':
                await self._validate_data_source_pid(pid=patch_document_list[i].value)
