# Contributors: Aure, Kowther
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

    def test_adding_a_question_success(self):
        self.login(email=self.renter.email, password=self.renter.password)
        response = self.client.post(
            'single_post/1',
            data=dict(renter_user_id=current_user.get_id(), post_id=1, question='question?'),
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)

    def test_adding_an_answer_success(self):
        self.login(email=self.propertyowner.email, password=self.propertyowner.password)
        response = self.client.post(
            '/answer/1',
            data=dict(property_owner_user_id=current_user.get_id(), comment_id=1, answer='answer',
                      current_user=current_user),
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
