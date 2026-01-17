from typing import Optional

from ftmcloud.cross_cutting.models.document import BaseDocument


class Report(BaseDocument):
    """
    Represents a request model that allows the user to specify a query.
    """
    pid: Optional[str]
    name: str
    submittedByUserPid: str

    class Config:
        scheme_extra = {
            "example": {
                "searchText": "Search Text",
                "productTypePid": "productTypePid",
                "limit": 10,
                "offset": 0,
                "requirements": [
                    {
                        "attributePid": "attributePid",
                        "value": {
                            "numValue": 4
                        }
                    }
                ]
            }
        }
