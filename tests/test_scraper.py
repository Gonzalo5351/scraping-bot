import unittest
import sys
import os

# Agrego el path al src del proyecto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from scraper import WorkanaScraper


class TestWorkanaScraper(unittest.TestCase):
    def test_instanciar_scraper(self):
        scraper = WorkanaScraper()
        self.assertIsInstance(scraper, WorkanaScraper)


if __name__ == '__main__':
    unittest.main()
