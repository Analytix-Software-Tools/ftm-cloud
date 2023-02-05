import statistics

from ftmcloud.core.config.config import Settings
from ftmcloud.core.exception.exception import FtmException
from ftmcloud.models.attribute import Attribute
from ftmcloud.models.product import Product
from ftmcloud.models.product_type import ProductType
from ftmcloud.models.reports import Hit, HitList


class ReportService:
    _hit_limit = Settings().MAX_QUERY_LIMIT

    def __init__(self):
        """
        Initialize the ReportService with any necessary collection instances.
        """
        self.products_collection = Product
        self.attributes_collection = Attribute
        self.product_types_collection = ProductType

    def _product_match_score(self, product, requirement_attr_pid_to_value, attribute_pid_mapping, attribute_pid_to_mean):
        """
        Assigns a product match score to the given product based on its relevance to the designated
        requirements. Attributes contribute to an overall product score, which ranges between -1 and 1
        based on the attribute type.

        :param product: the product to validate
        :param requirement_attr_pid_to_value: mapping of requirement attribute PIDs to values
        :param attribute_pid_mapping: attribute PIDs to attributes
        :return: an integer score for the product
        """
        product_score = 0
        for i in range(0, len(product.attributeValues)):
            if product.attributeValues[i].attributePid in requirement_attr_pid_to_value:
                data_type = attribute_pid_mapping[product.attributeValues[i].attributePid].type
                match data_type:
                    case "range":
                        min_value = requirement_attr_pid_to_value[product.attributeValues[i].attributePid].minValue
                        max_value = requirement_attr_pid_to_value[product.attributeValues[i].attributePid].maxValue
                        product_min_value = product.attributeValues[i].value.minValue
                        product_max_value = product.attributeValues[i].value.maxValue

                        if min_value == product_min_value and max_value == product_max_value:
                            product_score += 1

                        elif min_value < product_min_value and max_value > product_max_value:
                            product_score - (1 / (product_min_value - min_value)) + (
                                    1 / (max_value - product_max_value))
                        elif product_max_value > max_value and product_min_value < min_value:
                            product_score += (
                                    (1 / (product_max_value - max_value)) + (1 / (min_value - product_min_value)))
                        else:
                            product_score -= 1
                        break
                    case "number":
                        requirement_value = requirement_attr_pid_to_value[
                            product.attributeValues[i].attributePid].numValue
                        product_value = product.attributeValues[i].value.numValue

                        if requirement_value == product_value:
                            product_score += 1
                        else:
                            if product.attributeValues[i].attributePid in attribute_pid_to_mean \
                                    and attribute_pid_to_mean[product.attributeValues[i].attributePid] != 0:
                                product_score += (1 / abs(product.attributeValues[i].value.numValue
                                                          - attribute_pid_to_mean[product.attributeValues[i]
                                                          .attributePid]))
                        break
                    case "boolean":
                        if requirement_attr_pid_to_value[product.attributeValues[i].attributePid].value.value == \
                                product.attributeValues[i].value.value:
                            product_score += 1
                        else:
                            product_score -= 1
                    case "dropdown":
                        requirement_values = product.attributeValues[i].value.options
                        requirement_values = requirement_attr_pid_to_value[
                            product.attributeValues[i].attributePid
                        ].value.options
                        match = any(lambda x: x in requirement_values for x in requirement_values)
                        if match:
                            product_score += 1
                        else:
                            product_score -= 1
                        break
                    case "text":
                        # Rank based on levenshtein distance formula.
                        if requirement_attr_pid_to_value[product.attributeValues[i].attributePid].value.value == \
                                product.attributeValues[i].value.value:
                            product_score += 1
                        break
        return product_score

    def  _rank_product_hits(self, products, requirement_attr_pid_to_value, attribute_pid_mapping, attribute_pid_to_mean):
        """
        For each product in the subset, cross-references the attribute data type. Applies a variance
        matching algorithm for numbers and ranges and a string matching. Begins each product with
        a 0 score, indicating a neutral attribute value match. Each attribute match contributes
        to an overall score of the product.

        :param requirement_attr_pid_to_value: mapping of attribute pid to value in the products
        :param products:
        :param attribute_pid_mapping:
        :return: a list of hits
        """
        hits = []
        for i in range(0, len(products)):
            product_score = self._product_match_score(products[i], requirement_attr_pid_to_value,
                                                      attribute_pid_mapping, attribute_pid_to_mean)
            hit = Hit(hit=products[i], score=product_score)
            hits.append(hit)
        hits.sort(key=lambda x: x.score, reverse=True)

        return hits

    def _generate_attr_pid_to_mean(self, products, attribute_pid_mapping):
        """
        Generates a mapping of attribute PIDs to the mean value for attribute values which
        are of type AttributeNumberValue and exist within the potential product domain.

        :param products: represents the products to check
        :param attribute_pid_mapping: represents a mapping of attribute pids to attributes
        :return: a mapping of attribute PIDs to mean
        """
        attribute_pid_to_values = {}
        attribute_pid_to_mean = {} 
        attribute_pids = []
        for i in range(0, len(products)):
            for j in range(0, len(products[i].attributeValues)):
                if products[i].attributeValues[j].attributePid in attribute_pid_mapping \
                        and attribute_pid_mapping[products[i].attributeValues[j].attributePid].type == "number":
                    attribute_value = products[i].attributeValues[j]
                    if attribute_value.attributePid not in attribute_pid_to_values:
                        attribute_pid_to_values[attribute_value.attributePid] = []
                        attribute_pids.append(attribute_value.attributePid)
                    attribute_pid_to_values[attribute_value.attributePid].append(attribute_value.value.numValue)
        for k in range(0,len(attribute_pids)):
            attribute_pid_to_mean[attribute_pids[k]] = statistics.mean(attribute_pid_to_values[attribute_pids[k]])

        return attribute_pid_to_mean

    async def search_products(self, searchText=None, productTypePid=None, limit=_hit_limit, requirements=None):
        """
        Searches products and ranks each product based upon relevance. First, identifies a subset
        of the products that match the user's search text, product type and attribute requirements. Then,
        with that subset, applies a scoring algorithm which will rank by relevance. Finally, returns the
        list of hits sorted by the resulting score.

        :param searchText: represents the text being searched for
        :param limit: represents the max number of hits allowed
        :param requirements: an array of attribute value requirements
        :return: a list of hits
        """
        if searchText == "" or searchText is None:
            raise FtmException('exception.query.InvalidQuery', developer_message="Invalid search query!")
        if limit > self._hit_limit:
            limit = self._hit_limit
        product_type_exists = await self.product_types_collection.find_one({"pid": productTypePid,
                                                                            "isDeleted": {"$ne": True}})
        if product_type_exists is None:
            raise FtmException('exception.producttype.NotFound', developer_message="Invalid product type specified!",
                               user_message="Invalid product type specified!")
        attribute_pid_mapping = {}
        requirement_attr_pid_to_value = {}
        attribute_pids = []
        has_attributes = False
        attributes = await self.attributes_collection.find_all().to_list()
        for i in range(0, len(attributes)):
            attribute_pid_mapping[attributes[i].pid] = attributes[i]
        for j in range(0, len(requirements)):
            if requirements[j].attributePid not in attribute_pid_mapping:
                raise FtmException('exception.query.InvalidQuery', developer_message="Invalid search query specified!")
            else:
                requirement_attr_pid_to_value[requirements[j].attributePid] = requirements[j].value
                attribute_pids.append(requirements[j].attributePid)
                if not has_attributes:
                    has_attributes = True
        if not has_attributes:
            raise FtmException('exception.query.InvalidQuery', developer_message="Requirements length must be > 0!",
                               user_message="You must specify at least one attribute in your requirement!")
        query = {"name": {"$regex": searchText, "$options": "i"},
                 "productTypePid": productTypePid,
                 "isDeleted": {"$ne": True},
                 "attributeValues.attributePid": {"$in": attribute_pids}}
        products = await self.products_collection.find(query).to_list()
        attribute_pid_to_mean = self._generate_attr_pid_to_mean(products, attribute_pid_mapping)
        hits = self._rank_product_hits(products=products,
                                       requirement_attr_pid_to_value=requirement_attr_pid_to_value,
                                       attribute_pid_mapping=attribute_pid_mapping,
                                       attribute_pid_to_mean=attribute_pid_to_mean)
        results = HitList(hits=hits, maxScore=hits[0].score, total=len(hits))
        return results
