import unittest
import os

from generate import generate_html, create_html_file, read_file, get_jinja_env

FOLDER_PATH = 'test/source'

class TestGenerator(unittest.TestCase):
    def test_generate_html_valid_input(self):
        metadata = dict(
            title='Test invalid input',
            layout='home.html',
            content='Some content'
        )
        actual_result = generate_html(metadata, get_jinja_env(FOLDER_PATH))
        expected_result = '<h1>Test invalid input</h1>\nSome content\nfooter of the homepage\n'

        self.assertEqual(actual_result, expected_result)

    def test_generate_html_invalid_input(self):
        metadata = dict(
            title='Test invalid input',
            content='Some content'
        )
        actual_result = generate_html(metadata, get_jinja_env(FOLDER_PATH))
        expected_result = None

        self.assertEqual(expected_result, actual_result)

    def test_create_html_file(self):
        create_html_file('test', 'mocked html', 'output')
        self.assertEqual(True, os.path.exists('output/test.html'))

    def test_read_file(self):
        actual_result = read_file('test/source/contact.rst')
        expected_result = {'title': 'Contact us!', 'layout': 'base.html', 'content': '\nWrite an email to contact@example.com.\n'}
        self.assertDictEqual(expected_result, actual_result)