import unittest
from app.services import fetch_favicon


class TestFavicon(unittest.TestCase):
    def test_favicon_error(self):
        data = fetch_favicon("https://106.55.91.130/")
        self.assertFalse(data)

    def test_favicon(self):
        data = fetch_favicon("https://www.qq.com/")
        if not data:
            self.skipTest("unable to fetch favicon (network/site change)")
        self.assertIn("hash", data)
        self.assertIsInstance(data["hash"], int)


if __name__ == '__main__':
    unittest.main()
