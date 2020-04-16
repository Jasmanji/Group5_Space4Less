from tests.test_main import BaseTestCase
from flask_login import current_user


class TestPosts(BaseTestCase):

    def test_adding_a_post_success(self):
        self.login(email=self.propertyowner.email, password=self.propertyowner.password)
        response = self.client.post(
            '/post',
            data=dict(title='post1', content='content', location='location', space_size='M', current_user=current_user),
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
