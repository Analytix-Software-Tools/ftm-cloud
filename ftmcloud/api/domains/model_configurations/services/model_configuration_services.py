from ftmcloud.core.exception.exception import FtmException
from ftmcloud.core.service import Service
from ftmcloud.models.domains.categories.category import Category
from ftmcloud.models.domains.attributes.attribute import Attribute
from ftmcloud.models.domains.organizations.organization import Organization
from ftmcloud.models.domains.model_configurations.model_configuration import ModelConfiguration
from ftmcloud.models.domains.product_types.product_type import ProductType


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
