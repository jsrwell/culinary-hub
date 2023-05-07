from .base import AuthorsBaseTest
import pytest


@pytest.mark.functional_test
class AuthorsRegisterTest(AuthorsBaseTest):
    def test_the_test(self):
        self.browser.get(self.live_server_url + '/authors/register/')
        self.sleep()
