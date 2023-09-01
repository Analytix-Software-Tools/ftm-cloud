from ftmcloud.core.elastic.elastic import ElasticSearchIndexConnector
from ftmcloud.core.exception.exception import FtmException
from ftmcloud.core.service import AbstractService
from elasticsearch import AsyncElasticsearch


class SearchService(AbstractService):

    def __init__(self):
        """
        Initialize the SearchService.
        """
        super().__init__()
        self.es_connector = ElasticSearchIndexConnector("search-analytix-mongo-prod")

    async def search(
            self,
            q: str, 
            limit: int,
            offset: int,
            include_totals: int,
            additional_filters: int,
            fields: list[dict]
    ):
        """
        Searches domains for the specified text.

        :param: index the index to search
        :param: q the query
        :param: fields the fields to include for limiting data
        :param: limit the limit to data returned in one call
        :param: offset the offset from index 0
        :param: include_totals whether to include totals in the response
        :param: additional_filters additional filters to pass outside the response
        :return: the search query results
        """

        return await self.es_connector.query_index(
            q={"match": q},
            filter_path=None,
            offset=offset,
            limit=limit,
            include_totals=include_totals,
            additional_filters=additional_filters,
        )

