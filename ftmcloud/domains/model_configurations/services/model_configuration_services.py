from ftmcloud.core.exception.exception import FtmException
from ftmcloud.cross_cutting.service.service import Service
from ftmcloud.domains.categories.models.models import Category
from ftmcloud.domains.attributes.models.models import Attribute
from ftmcloud.domains.organizations.models.models import Organization
from ftmcloud.domains.model_configurations.models.models import ModelConfiguration
from ftmcloud.domains.product_types.models.models import ProductType


class ModelConfigurationsService(Service):

    def __init__(self):
        super(ModelConfigurationsService, self).__init__(collection=ModelConfiguration)

    async def add_document(self, new_document: ModelConfiguration):
        collection_model_mapping = {
            "attributes": Attribute,
            "categories": Category,
            "organizations": Organization,
            "product_types": ProductType
        }
        if new_document.targetCollection not in collection_model_mapping.keys():
            raise FtmException("error.model_configuration.InvalidModelConfiguration",
                               developer_message="Target collection is invalid.")
        document_exists = await collection_model_mapping[new_document.targetCollection].find_one(
            self.process_q(q=None, additional_filters={"pid": new_document.documentPid})
        )
        if document_exists is None:
            raise FtmException("error.model_configuration.InvalidModelConfiguration")
        await super(ModelConfigurationsService, self).add_document(new_document=new_document)
