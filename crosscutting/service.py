import json

from fastapi import HTTPException
from jsonpatch import JsonPatch, JsonPatchException

import uuid
from pydantic.error_wrappers import ValidationError

from config.config import Settings


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
        exists = self.collection.find_one(q)
        if exists is None:
            raise HTTPException(status_code=404, detail="Resource not found")

    async def add_document(self, new_document):
        """Adds a specified document.

        :param new_document:
        :param validation:
        :return:
        """
        new_pid = str(uuid.uuid4())
        new_document.pid = new_pid
        document = await new_document.create()
        return document

    async def get_all(self, q=None, offset=None, sort=None, limit=Settings().MAX_QUERY_LIMIT, additional_filters=None):
        """Retrieves all documents in the collection.

        :param additional_filters: A dict query applied after the q.
        :param q: Represents a stringify-d JSON to be processed as a query param.
        :param offset: Represents the offset from the initial document in the collection.
        :param sort: The field to sort by.
        :param limit: The max number of documents returned from the request.
        :return: The list of documents.
        """
        query = {}
        if q is not None:
            query = json.loads(q)
        if additional_filters is not None:
            query = {**query, **additional_filters}
        documents = await self.collection.find({"isDeleted": {"$ne": True}, **query}, limit=limit, skip=offset,
                                               sort=sort).to_list()
        return documents

    async def total(self, q=None, additional_filters=None):
        """Retrieves the total of documents that fit the specified criteria.

        :param q: Represents the stringified q object.
        :param additional_filters: Represents the additional filters to apply, if any.
        :return: The total count of documents matching the specified criteria.
        """
        query = {}
        if q is not None:
            query = json.loads(q)
        if additional_filters is not None:
            query = {**query, **additional_filters}
        return await self.collection.find(query).count()

    async def validate_exists(self, pid: str):
        """Validate the document exists.

        :param pid:
        :return:
        """
        exists = await self.collection.find_one({"isDeleted": {"$ne": True}, "pid": pid})
        if exists is None:
            raise HTTPException(status_code=404, detail=str(self.collection.__name__) + " not found.")
        return exists

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
        patch = JsonPatch(patch_document_list)
        patch_list = list(patch)
        for i in range(0, len(patch_list)):
            if patch_list[i]['path'] == '/_id' \
                    or patch_list[i]['path'] == '/pid' \
                    or patch_list[i]['path'] == '/isDeleted':
                raise HTTPException(status_code=422, detail="Invalid patch")
        result = await self.collection.find_one({"pid": pid})
        if result is None:
            raise HTTPException(status_code=404, detail="Resource not found.")
        try:
            diff_doc = patch.apply(result.dict())
            try:
                new_doc = self.collection(**diff_doc)
            except ValidationError:
                raise HTTPException(status_code=422, detail="Invalid patch")
            update_query = {"$set": {
                field: value for field, value in new_doc.dict().items() if field is not "id"
            }}
            await result.update(update_query)
        except JsonPatchException:
            raise HTTPException(status_code=422, detail="Patch list is of invalid or inoperable formatting.")

    async def delete_document(self, pid: str):
        """Delete the specified document by asserting the isDeleted field
        to be True. This helps to prevent a user accidentally deleting and
        mitigates fallout from any attacks.

        :param pid: The pid of the document to delete.
        :return: None
        """
        exists = await self.collection.find_one({"isDeleted": {"$ne": True}, "pid": pid})
        if exists is None:
            raise HTTPException(status_code=404, detail="Resource not found")
        await exists.update({"$set": {"isDeleted": True}})
