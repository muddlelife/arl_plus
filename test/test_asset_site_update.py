import unittest

from app import utils
from app.modules import TaskStatus, TaskType
from app.tasks.asset_site import AssetSiteUpdateTask


class TestAssetSiteMonitor(unittest.TestCase):

    def test_monitor(self):
        task_id = insert_task_data()
        scope_id = "63ac0a67d05e51e81a2d7577"
        task = AssetSiteUpdateTask(task_id=task_id, scope_id=scope_id)
        try:
            task.run()
        except Exception as e:
            if "没有找到" in str(e):
                self.skipTest("scope_id data not in DB: {}".format(e))
            raise


def insert_task_data():
    task_data = {
        'name': "测试资产分组更新",
        'target': "资产站点更新",
        'start_time': '-',
        'status': TaskStatus.WAITING,
        'type': TaskType.ASSET_SITE_UPDATE,
        "task_tag": TaskType.ASSET_SITE_UPDATE,
        'options': {
        },
        "end_time": "-",
        "service": [],
        "celery_id": "fake"
    }
    utils.conn_db('task').insert_one(task_data)
    task_id = str(task_data.pop("_id"))

    return task_id


if __name__ == '__main__':
    unittest.main()
