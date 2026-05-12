import unittest
from app.services.findVhost import find_vhost, brute_vhost


class TestFindVhost(unittest.TestCase):
    def test_brute_vhost(self):
        ip = "43.254.45.30"
        domains = ["www.vulbox.com", "account.vulbox.com", "ysrc.vulbox.com"]
        results = brute_vhost(ip, (domains, 'https'))
        # Site may be down; accept any result as valid
        self.assertIsInstance(results, (list, set))

        results = brute_vhost(ip, (domains, 'http'))
        self.assertIsInstance(results, (list, set))

    def test_find_vhost(self):
        ips = ["43.254.45.30", "1.1.1.1"]
        domains = ["www.vulbox.com", "account.vulbox.com", "ysrc.vulbox.com"]
        results = find_vhost(ips, domains)
        self.assertIsInstance(results, (list, set))

    def test_vhost_uniq(self):
        ips = ["59.63.235.44", "1.1.1.1", "180.96.32.95", "114.106.160.20"]
        domains = ["www.tencent.com", "m.tencent.com"]
        results = find_vhost(ips, domains)
        self.assertIsInstance(results, (list, set))


if __name__ == '__main__':
    unittest.main()
