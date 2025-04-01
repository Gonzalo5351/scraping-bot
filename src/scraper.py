import requests
from bs4 import BeautifulSoup
import re
import json

def limpiar_html(texto):
    """Elimina etiquetas HTML y espacios extras de un texto"""
    if not texto:
        return ""
    
    soup = BeautifulSoup(texto, "html.parser")

    # Eliminar scripts, estilos y metadatos no relevantes
    for elemento in soup(["script", "style", "meta", "nav", "footer"]):
        elemento.decompose()

    # Procesar enlaces y divisiones
    for tag in soup.find_all(["a", "div"]): #Procesar múltiples etiquetas
        if tag.name == "a":
            href = tag.get('href', '')
            # Solo mostrar URL si es relevante y no redundante
            if href and not href.startswith(('javascript:', '#')):
                tag.replace_with(f"{tag.get_text()} [URL]")  # Simplificamos la URL
        elif tag.name == "div":
            tag.replace_with(tag.get_text(" "))
    
    # Limpiar texto resultante
    texto_limpio = soup.get_text(" ", strip=True)
    
    # Eliminar líneas repetitivas (como categorías)
    lineas = [line.strip() for line in texto_limpio.splitlines() if line.strip()]
    lineas_unicas = []
    vistas = set()
    
    for linea in lineas:
        if linea not in vistas and not linea.startswith(("Categoria :", "Subcategoria :")):
            lineas_unicas.append(linea)
            vistas.add(linea)
    
    return "\n".join(lineas_unicas)


def obtener_ofertas_workana():
    """_summary_

    Returns:
        _type_: _description_
    """

    url = "https://www.workana.com/jobs?language=es"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        print(f"Accediendo a {url}...")
        response = requests.get(url, headers=headers)
        print(f"Código de estado HTTP: {response.status_code}")

        response.raise_for_status()
        
        # Extrae el JSON embebido
        script_data = re.search(r':results-initials=\'({.+?})\'', response.text)
        if not script_data:
            print("No se encontró el JSON embebido. HTML:", response.text[:500])  # Primeras 500 chars
            return []

        # Parsea el JSON y estructura las ofertas
        data = json.loads(script_data.group(1).replace('&quot;', '"'))
        ofertas = [{
            "titulo": limpiar_html(item.get("title", "Sin título")),
            "descripcion": limpiar_html(item.get("description", "Sin descripción")),
            "enlace": f"https://www.workana.com/job/{item.get('slug', '')}"
        } for item in data.get("results", [])]

        print(f"Ofertas encontradas: {len(ofertas)}")
        return ofertas
    
    except Exception as e:
        print(f"Error durante la ejecución: {e}")
        return []

if __name__ == "__main__":
    trabajos = obtener_ofertas_workana()

    if not trabajos:
        print("No se encontraron ofertas de trabajos.")

    for i, trabajo in enumerate(trabajos[:10], 1):  # Mostrar solo 5 resultados
        print(f"{i}. {trabajo['titulo']}")
        print(f"   {trabajo['descripcion']}")
        print(f"   {trabajo['enlace']}")
        print("-")