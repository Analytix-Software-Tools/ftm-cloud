import warnings

import elasticsearch.exceptions
from elasticsearch import Elasticsearch
from urllib3.exceptions import InsecureRequestWarning

from ftmcloud.core.config.config import Settings
from ftmcloud.core.exception.exception import FtmException
from ftmcloud.utils.query import validate_is_json


class ElasticSearchIndexConnector:

    def __init__(self, index_name: str):
        """
        Creates a new ElasticSearchConnectionManager.
        """
        self.config = Settings()
        self.index_name = index_name
        self.client = Elasticsearch(
            hosts=[self.config.ELASTICSEARCH_URI],
            http_auth=("elastic", "2GHZg07qwg6G7JlHY3f37N99"),
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
            additional_filters=None
    ):
        try:
            total_results = None
            results = []
            query = {}

            if q is not None:
                query = validate_is_json(q)

            if additional_filters is not None:
                query.update(additional_filters)

            documents = await self.client.search(
                index=self.index_name,
                query=q,
                size=limit,
                from_=offset
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
        ):
            raise FtmException("error.query.InvalidQuery")
