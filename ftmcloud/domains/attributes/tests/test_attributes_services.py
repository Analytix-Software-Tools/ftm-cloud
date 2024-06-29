import json
import unittest

from ftmcloud.domains.attributes.services.attribute_services import AttributesService


class TestAttributesServices(unittest.TestCase):
    """
    Test AttributesServices
    """
    def __init__(self):
        self._attributes_service = AttributesService()
        super().__init__()

    def success_response_valid_q(self):
        attribute_list_response = self._attributes_service.get_all(
            q=json.dumps({"name": "test"})
        )
        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
