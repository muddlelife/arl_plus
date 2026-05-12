import unittest
from app.services.githubSearch import github_search
from app.config import Config


class TestGithubSearch(unittest.TestCase):
    def test_github_search(self):
        if not Config.GITHUB_TOKEN:
            self.skipTest("GITHUB_TOKEN not configured")
        keyword = "1588080585"
        results = github_search(keyword)
        self.assertTrue(len(results) >= 1)
        result = results[0]
        self.assertTrue(result.commit_date)


if __name__ == '__main__':
    unittest.main()
