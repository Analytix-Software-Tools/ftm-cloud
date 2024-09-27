import unittest

from ftmcloud.domains.users.models.models import UserContact
from ftmcloud.domains.users.services.user_services import UserService


class TestUsersServices(unittest.TestCase):

    def setUp(self):
        self._service = UserService()

    def test_submit_user_contact_valid_form(self):

        contact = UserContact(
            issueType="a",
            message="testing",
            subject="a"
        )

        self._service.submit_user_contact(
            contact_form=contact
        )
