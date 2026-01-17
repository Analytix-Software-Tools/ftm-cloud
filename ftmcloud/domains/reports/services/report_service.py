from ftmcloud.core.config.config import Settings


class ReportService:
    _hit_limit = Settings().MAX_QUERY_LIMIT

    def __init__(self):
        """
        Initialize the ReportService with any necessary collection instances.
        """
