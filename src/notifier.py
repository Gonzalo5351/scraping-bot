# src/notifier.py
import os
import smtplib
from email.message import EmailMessage
from config import EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECEIVER


class EmailNotifier:
    def __init__(
        self, sender=EMAIL_SENDER, password=EMAIL_PASSWORD, receiver=EMAIL_RECEIVER
    ):
        self.sender = os.getenv("EMAIL_SENDER")
        self.password = os.getenv("EMAIL_PASSWORD")
        self.receiver = os.getenv("EMAIL_RECEIVER")

        if not all([self.sender, self.password, self.receiver]):
            raise ValueError(
                "Faltan variables de entorno: EMAIL_SENDER, EMAIL_PASSWORD o EMAIL_RECEIVER"
            )

    def format_message(self, subject: str, body: str) -> EmailMessage:
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = self.sender
        msg["To"] = self.receiver
        msg.set_content(body)
        return msg

    def send_notification(self, subject: str, body: str) -> bool:
        try:
            msg = self.format_message(subject, body)
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(self.sender, self.password)
                smtp.send_message(msg)
            return True
        except Exception as e:
            print(f"[NOTIFIER ERROR] {e}")
            return False

    def notify_new_posts(self, posts: list[dict]) -> bool:
        if not posts:
            return False

        lines = ["Nuevas publicaciones encontradas:\n"]
        for post in posts:
            title = post.get("title", "Sin título")
            url = post.get("url", "Sin URL")
            lines.append(f"- {title}\n  {url}\n")

        body = "\n".join(lines)
        subject = f"[Bot Scraping] {len(posts)} nueva(s) publicación(es) encontrada(s)"
        return self.send_notification(subject, body)
