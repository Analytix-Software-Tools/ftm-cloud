import datetime
import json
from json import JSONDecodeError

from jsonpatch import JsonPatch, JsonPatchException

import uuid
from pydantic.error_wrappers import ValidationError

from ftmcloud.core.config.config import Settings
from ftmcloud.core.exception.exception import FtmException

settings = Settings()


class Service:

    def __init__(self, collection, base_model=None):
        """Initialize a new service.

        :param collection:
        :param base_model:
        """
        self.collection = collection
        self.base_model = base_model

    async def find_one(self, q):
        """Finds one by the specified query.

        :param q:
        :return:
        """
        exists = await self.collection.find_one({"isDeleted": {"$ne": True}, **q})
        return exists

    async def add_document(self, new_document):
        """Adds a specified document.

        :param new_document:
        :param validation:
        :return:
        """
        new_pid = str(uuid.uuid4())
        new_document.pid = new_pid
        new_document.createdAt = datetime.datetime.now()
        document = await new_document.create()
        return document


    def _parse_q_fields(self, fields):
        """
        Sanitizes and ensures the q fields are a string in JSON format.
        """
        try:
            return json.loads(fields)
        except JSONDecodeError:
            raise FtmException('error.query.InvalidQuery')

    async def get_all(self, q=None, offset=None, sort=None, limit=None,
                      additional_filters=None, fields=None):
        """Retrieves all documents in the collection.

        :param additional_filters: A dict query applied after the q.
        :param q: Represents a stringify-d JSON to be processed as a query param.
        :param offset: Represents the offset from the initial document in the collection.
        :param sort: The field to sort by.
        :param limit: The max number of documents returned from the request.
        :param fields: The fields to include in the request
        :return: The list of documents.
        """
        query = {}
        if q is not None:
            try:
                query = json.loads(q)
            except ValueError as E:
                raise FtmException('error.general.InvalidJson', developer_message=E.__str__())
        if additional_filters is not None:
            query = {**query, **additional_filters}
        config = Settings()
        if limit is None:
            limit = config.DEFAULT_QUERY_LIMIT
        elif limit > config.MAX_QUERY_LIMIT:
            limit = config.DEFAULT_QUERY_LIMIT
        sort_criteria = []
        if sort is not None:
            sort_direction = sort[0]
            if sort_direction != '^' and sort_direction != '-':
                raise FtmException('error.query.InvalidSort')
            sort_field = sort[1:]
            if sort_direction == '^':
                sort_direction = 1
            elif sort_direction == '-':
                sort_direction = -1
            sort_criteria.append((sort_field, sort_direction))
        if fields is not None:
            fields = self._parse_q_fields(fields=fields)
        documents = await self.collection.find({"isDeleted": {"$ne": True}, **query}, projection=fields, limit=limit, skip=offset,
                                               sort=sort_criteria).to_list()
        return documents

    async def total(self, q=None, additional_filters=None):
        """Retrieves the total of documents that fit the specified criteria.

        :param q: Represents the stringified q object.
        :param additional_filters: Represents the additional filters to apply, if any.
        :return: The total count of documents matching the specified criteria.
        """
        query = {}
        try:
            if q is not None:
                query = json.loads(q)
            if additional_filters is not None:
                query = {**query, **additional_filters}
        except ValueError as E:
            raise FtmException('error.general.InvalidJson', developer_message=E.__str__())
        return await self.collection.find(query, {"isDeleted": {"$ne": True}}).count()

    async def validate_exists(self, pid: str, additional_filters=None):
        """Validate the document exists.

        :param additional_filters:
        :param pid:
        :return:
        """
        query = {"isDeleted": {"$ne": True}}
        if pid is not None:
            query["pid"] = pid
        if additional_filters is not None:
            query = {**query, **additional_filters}
        exists = await self.collection.find_one(query)
        if exists is None:
            raise FtmException(f"error.{self.collection.__name__.lower()}.NotFound")
        return exists

    async def validate_pids_in_list(self, pid_list: [str]):
        """Validates multiple resource PIDs within one general list of PIDs.

        :param pid_list: the list of pids
        :return:
        """
        pid_list_len = len(pid_list)
        if pid_list_len:
            for i in range(0, pid_list_len):
                await self.validate_exists(pid=pid_list[i])

    async def patch(self, pid: str, patch_document_list: list):
        """Patch the resource within the space by pid. Attempts to
        construct a patch document from the list provided. If the formatting
        fits, attempts to find the resource, creates a diff doc, then attempts
        to construct a model with the diff doc. If any errors present, routes
        the errors back to the user.

        :param pid:
        :param patch_document_list:
        :return:
        """
        if len(patch_document_list) == 0:
            return
        patch = JsonPatch(list(map(lambda x: x.dict(), patch_document_list)))
        patch_list = list(patch)
        for i in range(0, len(patch_list)):
            if patch_list[i]['path'] == '/_id' \
                    or patch_list[i]['path'] == '/pid' \
                    or patch_list[i]['path'] == '/isDeleted':
                raise FtmException('error.patch.InvalidPatch')
        result = await self.collection.find_one({"pid": pid})
        if result is None:
            raise FtmException(f"error.{self.collection.__name__.lower()}.NotFound")
        try:
            diff_doc = patch.apply(result.dict())
            try:
                new_doc = self.collection(**diff_doc)
            except ValidationError:
                raise FtmException('error.patch.InvalidPatch')
            update_query = {"$set": {
                field: value for field, value in new_doc.dict().items() if field != "id"
            }}
            await result.update(update_query)
        except JsonPatchException:
            raise FtmException('error.patch.InvalidPatch')

    async def delete_document(self, pid: str):
        """Delete the specified document by asserting the isDeleted field
        to be True. This helps to prevent a user accidentally deleting and
        mitigates fallout from any attacks.

        :param pid: The pid of the document to delete.
        :return: None
        """
        exists = await self.collection.find_one({"isDeleted": {"$ne": True}, "pid": pid})
        if exists is None:
            raise FtmException(f"error.{self.collection.__name__.lower()}.NotFound")
        await exists.update({"$set": {"isDeleted": True}})
