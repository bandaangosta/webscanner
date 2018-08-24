import unittest

import webscanner


class WebscannerTestCase(unittest.TestCase):

    def setUp(self):
        self.app = webscanner.app.test_client()

    def test_index(self):
        rv = self.app.get('/')
        self.assertIn('Welcome to Web Scanner FrontEnd', rv.data.decode())


if __name__ == '__main__':
    unittest.main()
