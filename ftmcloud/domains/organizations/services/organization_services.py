from ftmcloud.core.exception.exception import FtmException
from ftmcloud.cross_cutting.service.service import Service
from ftmcloud.domains.industries.models.models import Industry
from ftmcloud.domains.organizations.models.models import Organization


class OrganizationsService(Service):

    def __init__(self):
        super(OrganizationsService, self).__init__(collection=Organization)

    async def patch(self, pid: str, patch_document_list: list):
        for i in range(0, len(patch_document_list)):
            if patch_document_list[i].path == '/industryPids':
                patch_len = len(patch_document_list[i].value)
                for j in range(0, patch_len):
                    exists = await Industry.find_one({"pid": patch_document_list[i].value[j], "isDeleted": {"$ne": "true"}})
                    if exists is None:
                        raise FtmException('error.industry.NotFound')
        await super(OrganizationsService, self).patch(pid=pid, patch_document_list=patch_document_list)
