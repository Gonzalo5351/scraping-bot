import requests
from bs4 import BeautifulSoup
import re
import json
from typing import List, Dict


class WorkanaScraper:
    def __init__(self):
        self.url = "https://www.workana.com/jobs?language=es"
        self.headers = {"User-Agent": "Mozilla/5.0"}

    def get_jobs(self) -> List[Dict]:
        """Obtiene las ofertas de Workana y las retorna como una lista de diccionarios"""
        print(f"Accediendo a {self.url}...")
        try:
            response = requests.get(self.url, headers=self.headers)
            print(f"Código de estado HTTP: {response.status_code}")
            response.raise_for_status()

            script_data = re.search(r':results-initials=\'({.+?})\'', response.text)
            if not script_data:
                print("No se encontró el JSON embebido.")
                return []

            data = json.loads(script_data.group(1).replace('&quot;', '"'))

            ofertas = []
            for item in data.get("results", []):
                oferta = {
                    "title": self._clean_html(item.get("title", "Sin título")),
                    "description": self._clean_html(item.get("description", "Sin descripción")),
                    "link": f"https://www.workana.com/job/{item.get('slug', '')}"
                }
                ofertas.append(oferta)

            print(f"Ofertas encontradas: {len(ofertas)}")
            return ofertas

        except Exception as e:
            print(f"Error durante la ejecución: {e}")
            return []

    def _clean_html(self, text: str) -> str:
        """Limpia HTML y texto redundante de la descripción o título"""
        if not text:
            return ""

        soup = BeautifulSoup(text, "html.parser")

        # Remover elementos innecesarios
        for tag in soup(["script", "style", "meta", "nav", "footer"]):
            tag.decompose()

        for tag in soup.find_all(["a", "div"]):
            if tag.name == "a":
                href = tag.get('href', '')
                if href and not href.startswith(('javascript:', '#')):
                    tag.replace_with(f"{tag.get_text()} [URL]")
            elif tag.name == "div":
                tag.replace_with(tag.get_text(" "))

        texto_limpio = soup.get_text(" ", strip=True)
        lineas = [line.strip() for line in texto_limpio.splitlines() if line.strip()]
        lineas_unicas = []
        vistas = set()

        for linea in lineas:
            if linea not in vistas and not linea.startswith(("Categoria :", "Subcategoria :")):
                lineas_unicas.append(linea)
                vistas.add(linea)

        return "\n".join(lineas_unicas)
