from models.httperror import HttpError

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
        "description": "Internal server error"
    },
    503: {
        "model": HttpError,
        "description": "Service unavailable"
    }
}
