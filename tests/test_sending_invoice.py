from tests.test_main import BaseTestCase
from flask_login import current_user

class TestSendInvoice(BaseTestCase):

    def test_sending_invoice_success(self):
        self.login(email=self.propertyowner.email, password=self.propertyowner.password)
        response = self.client.post(
            '/send invoice/1',
            data=dict(price=100),
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
