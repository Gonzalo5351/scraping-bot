from scrapers.workana_scraper import WorkanaScraper
from programmer_profile import ProgrammerProfile
from study_roadmap import StudyRoadmap
from filter_engine import FilterEngine
from notifier import EmailNotifier
from config import (
    PROFILE_PATH,
    ROADMAP_PATH,
    EMAIL_SENDER,
    EMAIL_PASSWORD,
    EMAIL_RECEIVER,
)
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

# Enviar notificación por mail si hay trabajos relevantes
if resultados["relevant_jobs"]:
    notifier = EmailNotifier(
        sender=EMAIL_SENDER, password=EMAIL_PASSWORD, receiver=EMAIL_RECEIVER
    )

    subject = "🎯 Nuevas oportunidades relevantes encontradas"
    body = "\n".join(
        [f"- {job['title']} → {job['link']}" for job in resultados["relevant_jobs"]]
    )

    if notifier.send_notification(subject, body):
        logger.info("Correo enviado correctamente.")
    else:
        logger.error("No se pudo enviar el correo.")
else:
    logger.info("No se encontraron trabajos relevantes. No se envía correo.")
