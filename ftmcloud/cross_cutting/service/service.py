import datetime
import json
import logging
from json import JSONDecodeError
from copy import deepcopy

from jsonpatch import JsonPatch, JsonPatchException

import uuid

from pydantic.error_wrappers import ValidationError

from ftmcloud.core.config.config import Settings
from ftmcloud.core.exception.exception import FtmException
from ftmcloud.domains.users.models.models import User


class AbstractService:

    _logger = None

    def __init__(self):
        """
        AbstractService provides general purpose utilities to be used across different
        types of domains.
        """
        self.settings = Settings()
        self._logger = logging.getLogger(self.__class__.__name__)

    @staticmethod
    def validate_is_json(raw):
        """
        Validates the raw string is a JSON.
        """
        try:
            return json.loads(raw)
        except JSONDecodeError as E:
            raise FtmException("error.general.InvalidJson", developer_message=E.__str__())


class Service(AbstractService):

    def __init__(self, collection, base_model=None):
        """Initialize a service which provides create-read-update-delete functionality
        against a mongo collection.

        :param collection:
        :param base_model:
        """
        super().__init__()
        self.collection = collection
        self.base_model = base_model

    async def find_one(self, q):
        """Finds one by the specified query.

        :param q:
        :return:
        """
        exists = await self.collection.find_one({"isDeleted": {"$ne": "true"}, **q})
        return exists

    async def add_validator(self, new_document):
        """ Validates new document incoming.

        :param new_document: model_cls
            the new document
        :return:
        """
        pass

    async def add_document(self, new_document):
        """Adds a specified document.

        :param new_document:
        :param validation:
        :return:
        """
        await self.add_validator(new_document)
        new_pid = str(uuid.uuid4())
        new_document.pid = new_pid
        new_document.createdAt = datetime.datetime.now()
        document = await new_document.create()
        return document

    async def insert_documents(self, documents):
        """Adds many documents.

        :param documents: List[dict]
            list of documents to add

        :return:
        """
        insert_docs = []
        for _document in documents:
            new_pid = str(uuid.uuid4())
            _document.pid = new_pid
            _document.createdAt = datetime.datetime.now()
            insert_docs.append(_document)
        await self.collection.insert_many(insert_docs)

    def process_q(self, q, additional_filters):
        """
        Parse the q, combine additional filters and add the default
        delete filter.
        """
        deleted_filter = {"isDeleted": {"$ne": "true"}}
        if q is not None:
            # TODO: Should sanitize the query for invalid query values to prevent abuse.
            # self._sanitize_query(q)

            # TODO: Should create a datetime query if one is found.
            # q = self._create_datetime_query(json.dumps(q))

            q_list = [self.validate_is_json(q)]
        else:
            q_list = []

        q_list.append(deleted_filter)

        if additional_filters is not None:
            q_list.append(additional_filters)

        if len(q_list) > 1:
            q = {"$and": q_list}
        else:
            q = q_list[0]

        return q

    def get_projection_model_from_fields(self, fields):
        """
        Acts as a factory method to generate a projection model instance with a subset
        of collection fields.
        """
        projection_model = deepcopy(self.collection)
        field_values = fields.values()

        if all(x == "1" for x in field_values):
            is_inclusion = True
        elif all(x == "0" for x in field_values):
            is_inclusion = False
        else:
            raise FtmException("error.user.InvalidQuery")

        field_name_map = {}
        for field in self.collection.__fields__.keys():
            field_name_map[field] = True

        new_fields = {} if is_inclusion else self.collection.__fields__

        for key in fields.keys():
            if is_inclusion and key in field_name_map:
                new_fields[key] = self.collection.__fields__[key]
            elif not is_inclusion and key in field_name_map:
                new_fields.pop(key)
            else:
                raise FtmException("error.query.InvalidQuery")

        projection_model.__fields__ = new_fields
        projection_model.init_fields()

        return projection_model

    async def get_all(self, q=None, offset=None, sort=None, limit=None,
                      additional_filters=None):
        """Retrieves all documents in the collection.

        :param additional_filters: A dict query applied after the q.
        :param q: Represents a stringify-d JSON to be processed as a query param.
        :param offset: Represents the offset from the initial document in the collection.
        :param sort: The field to sort by.
        :param limit: The max number of documents returned from the request.
        :param fields: The fields to include in the request
        :return: The list of documents.
        """

        query = self.process_q(q=q, additional_filters=additional_filters)

        config = self.settings
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

        documents = await self.collection.find(query, limit=limit, skip=offset, sort=sort_criteria).to_list()

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
        return await self.collection.find(query, {"isDeleted": {"$ne": "true"}}).count()

    async def validate_exists(self, pid: str, additional_filters=None):
        """Validate the document exists.

        :param additional_filters:
        :param pid:
        :return:
        """
        query = {"isDeleted": {"$ne": "true"}}
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

    async def patch_document_validator(self, document, patch_document_list, current_user: User | None = None):
        """ This function allows a passthru to validate patch documents in the list before
        the patch is performed.

        :param document: dict
            the document
        :param patch_document_list: list[dict]
            list of json patch document
        :param current_user: User | None
            the current user

        :return:
        """
        pass

    async def patch(self, pid: str, patch_document_list: list, current_user: User | None = None):
        """Patch the resource within the space by pid. Attempts to
        construct a patch document from the list provided. If the formatting
        fits, attempts to find the resource, creates a diff doc, then attempts
        to construct a model with the diff doc. If any errors present, routes
        the errors back to the user.

        :param pid:
        :param patch_document_list:
        :param current_user: User | None
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
        await self.patch_document_validator(result, patch_list, current_user)
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

    async def delete_document(self, pid: str, additional_filters: dict = None):
        """Delete the specified document by asserting the isDeleted field
        to be True. This helps to prevent a user accidentally deleting and
        mitigates fallout from any attacks.

        :param pid: The pid of the document to delete.
        :param additional_filters: Additional filters to use on the documents
        :return: None
        """
        q = self.process_q(q={"pid": pid}, additional_filters=additional_filters)
        exists = await self.collection.find_one(q)
        if exists is None:
            raise FtmException(f"error.{self.collection.__name__.lower()}.NotFound")
        await exists.update({"$set": {"isDeleted": "true"}})
