from ftmcloud.core.exception.exception import FtmException
from ftmcloud.cross_cutting.models.document import BaseDocument


class Repository:
    """
    Class which allows for uniform access to the database.
    """

    _model_cls = None

    def __init__(self, model_cls):
        """ Abstracts the data layer away so that services can interact in a manner
        that is decoupled from the underlying implementation.

        :param model_cls: the model_cls to reference
        """
        self._model_cls = model_cls

    async def find(self, query, first, internal=False):
        """ Finds the specified document in the class.

        :param query:
        :param first:
        :param internal: bool
            whether request is being performed internally
        :return:
        """
        try:
            if not internal:
                query['isDeleted'] = {'$ne': 'true'}
            return await self._model_cls.find(query, first=first)
        except Exception as E:
            raise FtmException from E

    async def aggregate(self, pipeline):
        """ Aggregate the collection.

        :param pipeline: list[dict]
            aggregation pipeline
        :return:
        """
        try:
            return await self._model_cls.aggregate(aggregation_pipeline=pipeline)
        except Exception as E:
            raise FtmException from E

    async def delete(self, query):
        """ Deletes document aligning with the specified query.

        :param query:
        :return:
        """
        try:
            return await self._model_cls.delete(query)
        except Exception as E:
            raise FtmException from E

    async def update(self, query, update):
        """ Performs an update query.

        :param query: the query to use
        :param update: the update to perform
        :return:
        """
        try:
            return await self._model_cls.update(query, update)
        except Exception as E:
            raise FtmException from E

    async def insert(self, new_document):
        """ Inserts a new document.

        :param new_document: the document to insert
        :return: None
        """
        try:
            return await self._model_cls.insert(new_document)
        except Exception as E:
            raise FtmException from E
