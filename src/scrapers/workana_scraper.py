from logger import get_logger
import requests
import re
import json
from typing import List, Dict
from base_scraper import BaseScraper

logger = get_logger("WorkanaScraper")


class WorkanaScraper(BaseScraper):
    def __init__(self):
        super().__init__("https://www.workana.com/jobs?language=es")
        self.headers = {"User-Agent": "Mozilla/5.0"}

    def get_jobs(self) -> List[Dict]:
        try:
            response = requests.get(self.base_url, headers=self.headers)
            logger.info(f"Código de estado HTTP: {response.status_code}")
            response.raise_for_status()

            script_data = re.search(r":results-initials=\'({.+?})\'", response.text)
            if not script_data:
                print("No se encontró el JSON embebido.")
                return []

            data = json.loads(script_data.group(1).replace("&quot;", '"'))

            ofertas = []
            for item in data.get("results", []):
                oferta = {
                    "title": self.clean_html(item.get("title", "Sin título")),
                    "description": self.clean_html(
                        item.get("description", "Sin descripción")
                    ),
                    "link": f"https://www.workana.com/job/{item.get('slug', '')}",
                }
                ofertas.append(oferta)

            print(f"Ofertas encontradas: {len(ofertas)}")
            return ofertas

        except Exception as e:
            print(f"Error durante la ejecución: {e}")
            return []


# AGREGAR EL clean_html
