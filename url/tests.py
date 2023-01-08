from unittest.mock import patch
from django.test import TestCase

from url.models import Url
from urlShortner.settings import SHORT_URL_LENGTH

class TestUrl(TestCase):
    def setUp(self):
        self.url = Url.objects.create(
            title='Test Title',
            description='Test description',
            original_url='http://example.com',
        )

    def test_was_shorted_at_creation(self):
        """Checks if a shortened url is created when adding a new url"""
        self.assertNotEqual(self.url.short_url, "")

    def test_short_url_length(self):
        """Checks if a shortened url is created when adding a new url"""
        self.assertEqual(len(self.url.short_url), SHORT_URL_LENGTH)

    @patch('url.models.Url.generate_random_code', return_value='random_code')
    def test_short_url_is_return_of_generate_random_code(self, generate_random_code_mock):
        """Checks if the shortened url is created using the generated_random_code method"""
        url = Url.objects.create(
            title='Test Title',
            description='Test description',
            original_url='http://example.com',
        )

        self.assertEqual(url.short_url, generate_random_code_mock.return_value)

class TestRedirect(TestCase):
    def setUp(self):
        self.url = Url.objects.create(
            title='Test Title',
            description='Test description',
            original_url='http://example.com',
        )

    def test_redirect(self):
        """Checks if the client is redirected"""
        response = self.client.get(f'/{self.url.short_url}')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], self.url.original_url)

    def test_short_url_not_founded(self):
        """Checks if a 404 status code is returned to an invalid short url"""
        response = self.client.get('/any_short_url')
        self.assertEqual(response.status_code, 404)

class TestUseCounter(TestCase):
    def setUp(self):
        self.url = Url.objects.create(
            title='Test Title',
            description='Test description',
            original_url='http://example.com',
        )

    def test_access_a_url(self):
        """Checks if access a shorted url increments the counter"""
        self.client.get(f'/{self.url.short_url}')
        self.assertEqual(Url.objects.get(pk=self.url.pk).use_counter, 1)
