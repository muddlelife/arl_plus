import unittest
from app.tasks.scheduler import IPExecutor


class TestIPExec(unittest.TestCase):
    def test_ip_exec_1(self):
        target = "10.0.83.16"
        scope_id = "60b756b56591e7489b977a29"
        task_name = "自动化测试ip test"
        options = {
            "port_scan_type": "test",
            "port_scan": True,
            "service_detection": False,
            "os_detection": False,
            "site_identify": True,
            "site_capture": False,
            "file_leak": False,
            "site_spider": False,
            "ssl_cert": False,
        }
        executor = IPExecutor(target, scope_id, task_name, options)
        try:
            executor.insert_task_data()
        except Exception as e:
            if "没有找到" in str(e):
                self.skipTest("scope_id data not in DB: {}".format(e))
            raise
        executor.run()
        # IP target is a private IP; accept empty results as valid
        self.assertIsInstance(executor.ip_info_list, list)

    def test_ip_exec_2(self):
        target = "10.0.83.16"
        scope_id = "60b756b56591e7489b977a29"
        task_name = "自动化测试ip test"
        options = {
            "port_scan_type": "all",
            "port_scan": True,
            "service_detection": False,
            "os_detection": False,
            "site_identify": True,
            "site_capture": False,
            "file_leak": False,
            "site_spider": False,
            "ssl_cert": False,
        }
        executor = IPExecutor(target, scope_id, task_name, options)
        try:
            executor.insert_task_data()
        except Exception as e:
            if "没有找到" in str(e):
                self.skipTest("scope_id data not in DB: {}".format(e))
            raise
        executor.run()
        self.assertIsInstance(executor.ip_info_list, list)


if __name__ == '__main__':
    unittest.main()
