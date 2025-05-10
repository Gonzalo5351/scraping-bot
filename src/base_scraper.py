from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Union
import requests
import re
from bs4 import BeautifulSoup
from logger import get_logger

logger = get_logger("BaseScraper")


class BaseScraper(ABC):
    def __init__(self,  base_url: str,
        headers: Optional[Dict[str, str]] = None,
        expect_json: bool = False,
        regex_pattern: Optional[str] = None,):
                
        self.base_url = base_url
        self.headers = headers or {}
        self.expect_json = expect_json
        self.regex_pattern = regex_pattern
        logger.info(f"[BaseScraper] Inicializado para URL: {self.base_url}")

    def fetch_content(self) -> Union[str, Dict]:
        try:
            response = requests.get(self.base_url, headers=self.headers, timeout=10)
            logger.info(f"[BaseScraper] Código de estado HTTP: {response.status_code}")
            response.raise_for_status()

            if self.expect_json:
                return response.json()
            else:
                return response.text

        except requests.RequestException as e:
            logger.error(f"[BaseScraper] Error al hacer la solicitud: {e}")
            raise

    def extract_with_regex(self, text: str) -> Optional[re.Match]:
        if self.regex_pattern:
            match = re.search(self.regex_pattern, text)
            if match:
                logger.info("[BaseScraper] Regex encontró coincidencia.")
            else:
                logger.warning("[BaseScraper] Regex no encontró coincidencia.")
            return match
        return None
        
    @abstractmethod
    def parse_content(self, content: Union[str, Dict]) -> List[Dict]:
        """Extrae la información de interés del contenido"""
        pass

    def get_jobs(self) -> List[Dict]:
        content = self.fetch_content()
        return self.parse_content(content)
    
    @staticmethod
    def clean_html(text: str) -> str:
        """Limpia HTML y texto redundante."""
        if not text:
            return ""

        soup = BeautifulSoup(text, "html.parser")

        for tag in soup(["script", "style", "meta", "nav", "footer"]):
            tag.decompose()

        for tag in soup.find_all(["a", "div"]):
            if tag.name == "a":
                href = tag.get("href", "")
                if href and not href.startswith(("javascript:", "#")):
                    tag.replace_with(f"{tag.get_text()} [URL]")
            elif tag.name == "div":
                tag.replace_with(tag.get_text(" "))

        texto_limpio = soup.get_text(" ", strip=True)
        lineas = [line.strip() for line in texto_limpio.splitlines() if line.strip()]
        lineas_unicas = []
        vistas = set()

        for linea in lineas:
            if linea not in vistas and not linea.startswith(
                ("Categoria :", "Subcategoria :")
            ):
                lineas_unicas.append(linea)
                vistas.add(linea)

        return "\n".join(lineas_unicas)
