import os
import sys
import json
import pytest
from unittest.mock import patch

# Setup de paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
SCRAPING_BOT_SRC = os.path.join(BASE_DIR, "scraping-bot", "src")
DEVELOPER_PROFILE_SRC = os.path.join(BASE_DIR, "developer-profile", "src")
DEVELOPER_ROADMAP_SRC = os.path.join(BASE_DIR, "developer-roadmap", "src")

sys.path.insert(0, SCRAPING_BOT_SRC)
sys.path.insert(0, DEVELOPER_PROFILE_SRC)
sys.path.insert(0, DEVELOPER_ROADMAP_SRC)


@pytest.fixture
def setup_files():
    profile_path = os.path.join(SCRAPING_BOT_SRC, "test_profile.json")
    roadmap_path = os.path.join(SCRAPING_BOT_SRC, "test_roadmap.json")
    original_config_path = os.path.join(SCRAPING_BOT_SRC, "config.py")
    backup_config_path = os.path.join(SCRAPING_BOT_SRC, "config_backup.py")

    with open(profile_path, "w", encoding="utf-8") as f:
        json.dump({"skills": ["Python", "Git"]}, f)

    with open(roadmap_path, "w", encoding="utf-8") as f:
        json.dump({"skills": ["Scraping", "OOP"]}, f)

    if os.path.exists(original_config_path):
        os.rename(original_config_path, backup_config_path)

    with open(original_config_path, "w", encoding="utf-8") as f:
        f.write(f'PROFILE_PATH = r"{profile_path}"\n')
        f.write(f'ROADMAP_PATH = r"{roadmap_path}"\n')

    yield

    os.remove(profile_path)
    os.remove(roadmap_path)
    os.remove(original_config_path)
    if os.path.exists(backup_config_path):
        os.rename(backup_config_path, original_config_path)


def test_main_runs_without_crashing(setup_files):
    with (
        patch("scraper.WorkanaScraper.get_jobs", return_value=[]),
        patch(
            "filter_engine.FilterEngine.apply_filters",
            return_value={"relevant_jobs": [], "future_opportunities": []},
        ),
    ):
        try:
            import main
        except Exception as e:
            pytest.fail(f"main.py lanzó una excepción inesperada: {e}")
