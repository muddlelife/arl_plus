import os
import re
import time
from app import  utils
from app.config import Config
from .baseThread import BaseThread
logger = utils.get_logger()


def _phantomjs_bin():
    """Prefer the bundled phantomjs binary if present.

    Some environments (like Python 3.11 venv/unit tests) may not have phantomjs
    installed on PATH.
    """
    bundled = os.path.join(os.path.dirname(__file__), '..', 'tools', 'phantomjs')
    bundled = os.path.abspath(bundled)
    # Repo sometimes stores tools without +x. If the file exists, try using it.
    if os.path.isfile(bundled):
        return bundled
    return 'phantomjs'


class SiteScreenshot(BaseThread):
    def __init__(self, sites, concurrency=3, capture_dir = "./"):
        super().__init__(sites, concurrency = concurrency)
        self.capture_dir = capture_dir
        self.screenshot_map = {}

        os.makedirs(self.capture_dir, 0o777, True)

    def work(self, site):
        file_name = '{}/{}.jpg'.format(self.capture_dir, self.gen_filename(site))

        cmd_parameters = [_phantomjs_bin(),
                          '--ignore-ssl-errors true',
                          '--ssl-protocol any',
                          '--ssl-ciphers ALL',
                          Config.SCREENSHOT_JS,
                          '-u={}'.format(site),
                          '-s={}'.format(file_name),
                          ]
        logger.debug("screenshot {}".format(" ".join(cmd_parameters)))

        utils.exec_system(cmd_parameters)

        self.screenshot_map[site] = file_name

    def gen_filename(self, site):
        filename = site.replace('://', '_')

        return re.sub('[^\w\-_\. ]', '_', filename)

    def run(self):
        t1 = time.time()
        logger.info("start screen shot {}".format(len(self.targets)))
        self._run()
        elapse = time.time() - t1
        logger.info("end screen shot elapse {}".format(elapse))


def site_screenshot(sites, concurrency = 3, capture_dir="./"):
    s = SiteScreenshot(sites, concurrency = concurrency, capture_dir = capture_dir)
    s.run()
