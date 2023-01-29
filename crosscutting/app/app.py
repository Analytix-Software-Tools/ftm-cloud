from fastapi import FastAPI
from fastapi.routing import APIRoute
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from starlette.middleware.cors import CORSMiddleware

from config.config import limiter
from crosscutting.error.exception import handle_default_exceptions, configure_logging, FtmException


class FTMApi(FastAPI):
    """

    This is a class derived from FastAPI's base application class. This is intended to tie
    our application environment with the application context and initialize any configurations
    that need to run prior to listening for requests.

    """

    def __init__(self, routers=None, **kwargs):
        """

        Initializes a new instance of the application.

        :param kwargs: represents the kwargs associated with the FastAPI instance
        """

        if routers is None:
            routers = []

        def custom_generate_unique_id(route: APIRoute):
            return f"{route.name}"

        super().__init__(title="FTMCloud",
                         description="Search engine and analytics API.",
                         version="1.0.0",
                         generate_unique_id_function=custom_generate_unique_id, **kwargs)
        self.configure()
        self._routers = routers

    def configure(self):
        """

        Configures our application for running. Attaches exception handling and logging,
        configures routing, rate-limiting, and initializes the connection to the database.

        :return: None
        """
        configure_logging()
        self.state.limiter = limiter
        self.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
        self.add_exception_handler(Exception, handle_default_exceptions)
        self.add_exception_handler(FtmException, handle_default_exceptions)
        self.add_middleware(CORSMiddleware,
                            allow_origins=["*"],
                            allow_credentials=True,
                            allow_methods=["*"],
                            allow_headers=["*"],
                            expose_headers=['X-Total-Count'])
