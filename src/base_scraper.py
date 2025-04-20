from abc import ABC, abstractmethod
from typing import List, Dict
import re
from bs4 import BeautifulSoup
from logger import get_logger

logger = get_logger("BaseScraper")


class BaseScraper(ABC):
    def __init__(self, base_url: str):
        self.base_url = base_url
        logger.info(f"[BaseScraper] Inicializando con URL base: {self.base_url}")

    @abstractmethod
    def get_jobs(self) -> List[Dict]:
        """Debe devolver una lista de ofertas laborales."""
        pass

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
