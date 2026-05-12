import unittest
import os
from app.utils import get_ip_city, get_ip_asn


class TestGeoIP2(unittest.TestCase):
    def test_get_ip_city(self):
        city_path = "/data/GeoLite2/GeoLite2-City.mmdb"
        if not os.path.isfile(city_path):
            self.skipTest("GeoLite2-City.mmdb not found")
        r = get_ip_city("202.106.196.115")
        self.assertTrue(r["region_name"] == "Beijing")

    def test_get_ip_asn(self):
        asn_path = "/data/GeoLite2/GeoLite2-ASN.mmdb"
        if not os.path.isfile(asn_path):
            self.skipTest("GeoLite2-ASN.mmdb not found")
        r = get_ip_asn("202.106.196.115")
        self.assertTrue(r["number"] == 4808)


if __name__ == '__main__':
    unittest.main()
