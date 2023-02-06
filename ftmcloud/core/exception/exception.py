import logging
import sys
import traceback
import uuid

from fastapi.encoders import jsonable_encoder

from ftmcloud.models.httperror import HttpError
import yaml
from fastapi.responses import JSONResponse
from starlette.requests import Request


def configure_logging():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)


class FtmException(Exception):
    """
    An exception class which codifies and streamlines exception handling so that
    common exceptions can be displayed to the user more uniformly.
    """

    def __init__(self, error_code: str, developer_message=None, user_message=None, exception=None,
                 language_code: str = "en"):
        """
        Initialize the exception with the specified exception code. Load the errors
        YAML and attempt to parse the exception. The details of the exception are
        listed within the YML file.

        :param error_code: represents the application-specific code of the exception
        :param developer_message the developer message override
        :param user_message the user message override
        :param exception an instance of Exception to be caught and handled
        """
        Exception.__init__(self)

        if exception:
            self.with_traceback(exception.__traceback__)

        with open('ftmcloud/core/exception/errors.yaml', "r") as stream:
            try:
                error_messages = yaml.safe_load(stream=stream)
                if error_code not in error_messages['errors']:
                    raise ValueError('The exception class provided does not exist.')
                error = error_messages['errors'][error_code]
                self.error_code = error_code
                self.developer_message = developer_message if developer_message else error['developerMessage']
                self.user_message = user_message if user_message else error['userMessage']
                self.status_code = error['statusCode']
                self.info = error['info']

                if error['uuid']:
                    self.error_id = uuid.uuid4()
                else:
                    self.error_id = None

                self.traceback = error['traceback']

                match error['logLevel']:
                    case "CRITICAL":
                        self.log_level = logging.CRITICAL
                    case "ERROR":
                        self.log_level = logging.ERROR
                    case "WARNING":
                        self.log_level = logging.WARNING
                    case "INFO":
                        self.log_level = logging.INFO
                    case _:
                        raise ValueError('The logging level provided is invalid.')

            except yaml.YAMLError as exc:
                print(exc)

    def __json__(self):
        """

        Generates an HTTPResponse which is a JSON representation of the exception to be
        more easily consumed by an end user or developer. Initializes a Pydantic
        HttpError model which allows for easier serialization.

        :return: an JSONResponse
        """
        error = HttpError(
            developerMessage=self.developer_message,
            userMessage=self.user_message,
            statusCode=self.status_code,
            info=self.info,
            errorCode=self.error_code
        )
        return JSONResponse(content=jsonable_encoder(error), status_code=error.statusCode)

    def log(self):
        logger = logging.getLogger("Exception")
        logger.setLevel(self.log_level)
        log_msg = "Error Code: {}, Error ID: {}".format(self.error_code, self.error_id)
        if self.traceback:
            tracebacks = traceback.format_exception(FtmException, self, self.__traceback__)
            log_msg += "\n" + ''.join(tracebacks)
        logger.log(self.log_level, log_msg)


def handle_default_exceptions(request: Request, exc: Exception):
    """

    This function intercepts any exceptions that are called and converts them to
    an instance of FTMException so that they are returned in a standardized format
    to the user.

    :return:
    """
    if not isinstance(exc, FtmException):
        exc = FtmException(error_code="exception", exception=exc)
        exc.log()
    return exc.__json__()


default_exception_list = {
    401: {
        "model": HttpError,
        "description": "Invalid credentials"
    },
    403: {
        "model": HttpError,
        "description": "Insufficient permissions"
    },
    429: {
        "model": HttpError,
        "description": "Rate limit exceeded"
    },
    500: {
        "model": HttpError,
        "description": "Internal server exception"
    },
    503: {
        "model": HttpError,
        "description": "Service unavailable"
    }
}
