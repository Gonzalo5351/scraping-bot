from scrapers.workana_scraper import WorkanaScraper
from programmer_profile import ProgrammerProfile
from study_roadmap import StudyRoadmap
from filter_engine import FilterEngine
from config import PROFILE_PATH, ROADMAP_PATH
from logger import get_logger

logger = get_logger("Main")

# Cargar perfil y roadmap
profile = ProgrammerProfile(PROFILE_PATH)
roadmap = StudyRoadmap(ROADMAP_PATH)

# Scrapear ofertas
scraper = WorkanaScraper()
jobs = scraper.get_jobs()

# Filtrar ofertas
engine = FilterEngine(profile, roadmap)
resultados = engine.apply_filters(jobs)

# Mostrar resultados
print("\n=== Trabajos Relevantes ===")
for job in resultados["relevant_jobs"]:
    print(f"- {job['title']} → {job['link']}")

print("\n=== Oportunidades Futuras ===")
for job in resultados["future_opportunities"]:
    print(f"- {job['title']} → {job['link']}")
