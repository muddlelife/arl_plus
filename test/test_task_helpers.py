import unittest
from app.helpers.task import restart_task


class TestTaskHelpers(unittest.TestCase):
    def test_restart_task_error(self):
        task_id = "618121a56591e7084d649acb"
        try:
            restart_task(task_id)
        except Exception as e:
            self.assertTrue(task_id in str(e))

    def test_restart_task(self):
        task_id = "618267646591e708cdff207f"
        try:
            data = restart_task(task_id)
        except Exception as e:
            if "没有找到" in str(e):
                self.skipTest("task_id data not in DB: {}".format(e))
            raise
        self.assertTrue(isinstance(data, dict))


if __name__ == '__main__':
    unittest.main()
