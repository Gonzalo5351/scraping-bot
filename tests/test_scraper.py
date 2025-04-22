import os
import sys
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from scrapers import WorkanaScraper


def test_instanciar_scraper():
    scraper = WorkanaScraper()
    assert isinstance(scraper, WorkanaScraper)
