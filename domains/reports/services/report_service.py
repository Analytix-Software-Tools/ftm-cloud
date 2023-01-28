from config.config import Settings
from crosscutting.error.exception import FtmException
from models.attribute import Attribute
from fastapi import HTTPException
from models.product import Product
from models.product_type import ProductType
from models.reports import Hit, HitList


class ReportService:

    _hit_limit = Settings().MAX_QUERY_LIMIT

    def __init__(self):
        """
        Initialize the ReportService with any necessary collection instances.
        """
        self.products_collection = Product
        self.attributes_collection = Attribute
        self.product_types_collection = ProductType

    def _product_match_score(self, product, requirement_attr_pid_to_value, attribute_pid_mapping):
        """
        Assigns a product match score to the given product based on its relevance to the designated
        requirements. Max score per attribute varies between -n and n, where n is the number of times the
        attribute occurs within the product. The scoring system (per 1 instance of an attribute) is as follows:

        Boolean: assigned a score of 1 if exact match, for an opposite match, -1

        Number: assigned a score of 1 if exact match, otherwise assigned a score of 1 - distance(mean), where
        the mean refers to the mean value of all values for that attribute on that product type

        Range: assigned a score of 1 if exact match, otherwise 1 - abs(variance). only values within the query
        range are provided

        Dropdown/text: assigned a score based on a pattern matching technique. +1 for exact matches, otherwise
        1/deviation from the desired string. If there is no match, -1.

        :param product:
        :param requirement_attr_pid_to_value:
        :param attribute_pid_mapping:
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
                            product_score += 2

                        elif min_value < product_min_value and max_value > product_max_value:
                            product_score += (1 - (product_min_value - min_value)) + (
                                    1 - (max_value - product_max_value))
                        elif product_max_value > max_value and product_min_value < min_value:
                            product_score += (
                                    (1 - (product_max_value - max_value)) + (1 - (min_value - product_min_value)))
                        else:
                            product_score -= 1
                        break
                    case "number":
                        break
                    case "boolean":
                        break
                    case "dropdown":
                        break
                    case "text":
                        break
        return product_score

    def _rank_product_hits(self, products, requirement_attr_pid_to_value, attribute_pid_mapping):
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
            product_score = self._product_match_score(products[i], requirement_attr_pid_to_value, attribute_pid_mapping)
            hit = Hit(hit=products[i], score=product_score)
            hits.append(hit)
        hits.sort(key=lambda x: x.score)

        return hits

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
            # If no search text provided, raise an exception to the user.
            raise FtmException('error.query.InvalidQuery', developer_message="Invalid search query!")
        if limit > self._hit_limit:
            # Reset the limit where applicable.
            limit = self._hit_limit
        product_type_exists = await self.product_types_collection.find_one({"pid": productTypePid,
                                                                            "isDeleted": {"$ne": True}})
        if product_type_exists is None:
            raise FtmException('error.producttype.NotFound', developer_message="Invalid product type specified!",
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
                raise FtmException('error.query.InvalidQuery', developer_message="Invalid search query specified!")
            else:
                requirement_attr_pid_to_value[requirements[j].attributePid] = requirements[j].value
                attribute_pids.append(requirements[j].attributePid)
                if not has_attributes:
                    has_attributes = True
        query = {"name": {"$regex": searchText, "$options": "i"},
                 "productTypePid": productTypePid,
                 "isDeleted": {"$ne": True}}
        if has_attributes:
            query["attributeValues.attributePid"] = {"$in": attribute_pids}
        products = await self.products_collection.find(query).to_list()
        hits = self._rank_product_hits(products=products,
                                       requirement_attr_pid_to_value=requirement_attr_pid_to_value,
                                       attribute_pid_mapping=attribute_pid_mapping)
        results = HitList(hits=hits, maxScore=hits[0].score, total=len(hits))
        return results
