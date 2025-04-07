import unittest
import os
import sys
import json
from unittest.mock import patch, MagicMock

# Acceso a todos los módulos
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))

SCRAPING_BOT_SRC = os.path.join(BASE_DIR, 'scraping-bot', 'src')
DEVELOPER_PROFILE_SRC = os.path.join(BASE_DIR, 'developer-profile', 'src')
DEVELOPER_ROADMAP_SRC = os.path.join(BASE_DIR, 'developer-roadmap', 'src')

sys.path.insert(0, SCRAPING_BOT_SRC)
sys.path.insert(0, DEVELOPER_PROFILE_SRC)
sys.path.insert(0, DEVELOPER_ROADMAP_SRC)

class TestMainIntegration(unittest.TestCase):
    def setUp(self):
        # Creamos archivos temporales de perfil y roadmap
        self.profile_path = os.path.join(SCRAPING_BOT_SRC, 'test_profile.json')
        self.roadmap_path = os.path.join(SCRAPING_BOT_SRC, 'test_roadmap.json')

        with open(self.profile_path, 'w', encoding='utf-8') as f:
            json.dump({"skills": ["Python", "Git"]}, f)

        with open(self.roadmap_path, 'w', encoding='utf-8') as f:
            json.dump({"skills": ["Scraping", "OOP"]}, f)

        # Creamos un config.py temporal
        self.original_config_path = os.path.join(SCRAPING_BOT_SRC, 'config.py')
        self.backup_config_path = os.path.join(SCRAPING_BOT_SRC, 'config_backup.py')

        # Hacemos backup del config original si existe
        if os.path.exists(self.original_config_path):
            os.rename(self.original_config_path, self.backup_config_path)

        with open(self.original_config_path, 'w', encoding='utf-8') as f:
            f.write(f'PROFILE_PATH = r"{self.profile_path}"\n')
            f.write(f'ROADMAP_PATH = r"{self.roadmap_path}"\n')

    def tearDown(self):
        # Borrar archivos temporales
        os.remove(self.profile_path)
        os.remove(self.roadmap_path)
        os.remove(self.original_config_path)

        if os.path.exists(self.backup_config_path):
            os.rename(self.backup_config_path, self.original_config_path)

    def test_main_runs_without_crashing(self):
        with patch('scraper.WorkanaScraper.get_jobs', return_value=[]), \
             patch('filter_engine.FilterEngine.apply_filters', return_value={"relevant_jobs": [], "future_opportunities": []}):
            try:
                import main  # Esto ejecuta main.py
            except Exception as e:
                self.fail(f"main.py lanzó una excepción inesperada: {e}")
