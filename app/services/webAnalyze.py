import time
import json
import os
from app import utils
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


class WebAnalyze(BaseThread):
    def __init__(self, sites, concurrency=3):
        super().__init__(sites, concurrency = concurrency)
        self.analyze_map = {}

    def work(self, site):
        cmd_parameters = [_phantomjs_bin(),
                          '--ignore-ssl-errors true',
                          '--ssl-protocol any',
                          '--ssl-ciphers ALL',
                          Config.DRIVER_JS ,
                          site
                          ]
        logger.debug("WebAnalyze=> {}".format(" ".join(cmd_parameters)))

        output = utils.check_output(cmd_parameters, timeout=20)
        output = output.decode('utf-8')
        self.analyze_map[site] = json.loads(output)["applications"]

    def run(self):
        t1 = time.time()
        logger.info("start WebAnalyze {}".format(len(self.targets)))
        self._run()
        elapse = time.time() - t1
        logger.info("end WebAnalyze elapse {}".format(elapse))
        return self.analyze_map


def web_analyze(sites, concurrency=3):
    s = WebAnalyze(sites, concurrency=concurrency)
    return s.run()



