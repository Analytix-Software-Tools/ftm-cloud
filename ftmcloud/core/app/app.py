from fastapi import FastAPI
from fastapi.routing import APIRoute
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from starlette.middleware.cors import CORSMiddleware
from ftmcloud.core.config.config import Settings

from ftmcloud.core.config.config import limiter
from ftmcloud.core.exception.exception import handle_default_exceptions, configure_logging, FtmException


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

        self.configuration = Settings()

        def custom_generate_unique_id(route: APIRoute):
            return f"{route.name}"

        super().__init__(title=self.configuration.PROJECT_NAME,
                         description="Search engine and analytics API.",
                         version=self.configuration.API_REVISION,
                         debug=self.configuration.DEBUG,
                         servers=[
                             {
                                 "url": "https://api.analytix-software.com/v0"
                             }
                         ],
                         license_info={
                             "name": "GNU General Public License v3.0",
                             "url": "https://www.gnu.org/licenses/gpl-3.0.en.html",
                         },
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
