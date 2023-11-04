import elasticsearch.exceptions
from elasticsearch import Elasticsearch

from ftmcloud.core.config.config import Settings
from ftmcloud.core.exception.exception import FtmException
from ftmcloud.common.query.query import validate_is_json


class ElasticSearchIndexConnector:

    def __init__(self, index_name: str):
        """
        Creates a new ElasticSearchConnectionManager.
        """
        self.config = Settings()
        self.index_name = index_name
        self.client = Elasticsearch(
            hosts=[self.config.ELASTICSEARCH_URI],
            http_auth=("elastic", "1Lo52xdUi6FG344NgLC4yi18"),
            verify_certs=False,
        )

    def _suppress_warnings(self):
        """
        Suppress warnings from ElasticSearch.

        :return:
        """
        pass

    async def query_index(
            self,
            q=None,
            limit=10,
            offset=0,
            filter_path="",
            include_totals=None,
            additional_filters=None,
            fields=None,
    ):
        try:
            total_results = None
            results = []
            query = q

            if additional_filters is not None:
                query.update(additional_filters)

            documents = self.client.search(
                index=self.index_name,
                query=q,
                filter_path=filter_path,
                size=limit,
                from_=offset,
                fields=fields
            )

            if documents is not None:
                if include_totals is not None and 'hits' in documents and 'total' in documents['hits']:
                    total_results = documents['hits']['total']
                results = documents

            return results, total_results

        except (
                elasticsearch.exceptions.TransportError,
                elasticsearch.exceptions.SSLError
        ) as E:
            print(E)
            raise FtmException("error.search.ConnectionError")
        except (
                elasticsearch.exceptions.ApiError
        ) as E:
            print(str(E))
            raise FtmException("error.query.InvalidQuery")
