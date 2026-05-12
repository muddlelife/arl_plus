import unittest
from app import services
from app.services.infoHunter import InfoHunter


class TestWebInfoHunter(unittest.TestCase):
    def test_run_wih(self):
        if not InfoHunter([]).check_have_wih():
            self.skipTest("wih binary not available")
        sites = ["https://www.freebuf.com", "https://www.qq.com/"]
        results = services.run_wih(sites)

        for result in results:
            print(result)

        self.assertTrue(len(results) > 2)
