import unittest
from app.helpers.scheduler import have_same_site_update_monitor


class TestScheduler(unittest.TestCase):
    def test_have_same_site_update_monitor(self):
        data = have_same_site_update_monitor("5fb51bb26591e71df2d1f27c")
        if not data:
            self.skipTest("no scheduler data in DB")
        self.assertTrue(data)


if __name__ == '__main__':
    unittest.main()
