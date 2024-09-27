import json
from json import JSONDecodeError

from ftmcloud.core.exception.exception import FtmException


def validate_is_json(raw):
    """
    Validates the raw string is a JSON.
    """
    if isinstance(raw, dict):
        return raw

    try:
        return json.loads(raw)
    except JSONDecodeError as E:
        raise FtmException("error.general.InvalidJson", developer_message=E.__str__())