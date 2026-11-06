"""Sozlamalar .env faylidan (yoki muhit o'zgaruvchilaridan) o'qiladi."""
import os
from dataclasses import dataclass, field
from pathlib import Path

BASE = Path(__file__).parent


def _load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


_load_dotenv(BASE / ".env")


def _ids(raw: str) -> list[int]:
    out = []
    for part in raw.replace(";", ",").split(","):
        part = part.strip()
        if part.lstrip("-").isdigit():
            out.append(int(part))
    return out


@dataclass(frozen=True)
class Config:
    token: str = os.getenv("BOT_TOKEN", "")
    admin_ids: list[int] = field(default_factory=lambda: _ids(os.getenv("ADMIN_IDS", "")))
    # Arizalar shu chatga keladi (shaxsiy chat yoki guruh). Bo'sh bo'lsa — birinchi adminga.
    leads_chat_id: int | None = int(os.getenv("LEADS_CHAT_ID")) if os.getenv("LEADS_CHAT_ID", "").lstrip("-").isdigit() else None
    db_path: str = os.getenv("DB_PATH", str(BASE / "data" / "bot.sqlite3"))
    # Landing page manzili (https). Bo'lsa, menyuda "Sayt" tugmasi chiqadi va Telegram ichida Mini App bo'lib ochiladi.
    site_url: str = os.getenv("SITE_URL", "")
    # Ijtimoiy tarmoqlar (ixtiyoriy) — "Abror haqida" bo'limida tugma bo'lib chiqadi
    instagram_url: str = os.getenv("INSTAGRAM_URL", "")
    telegram_url: str = os.getenv("TELEGRAM_URL", "")
    youtube_url: str = os.getenv("YOUTUBE_URL", "")
    default_lang: str = os.getenv("DEFAULT_LANG", "uz")

    @property
    def notify_chat(self) -> int | None:
        return self.leads_chat_id or (self.admin_ids[0] if self.admin_ids else None)

    @property
    def links(self) -> list[tuple[str, str]]:
        return [(n, u) for n, u in (("Instagram", self.instagram_url),
                                     ("Telegram", self.telegram_url),
                                     ("YouTube", self.youtube_url)) if u]


cfg = Config()
