"""SQLite: foydalanuvchilar, arizalar, test natijalari, Telegram file_id keshi."""
from __future__ import annotations

import csv
import io
from datetime import datetime, timezone
from pathlib import Path

import aiosqlite

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id          INTEGER PRIMARY KEY,
    username    TEXT,
    full_name   TEXT,
    lang        TEXT,
    source      TEXT,
    created_at  TEXT,
    last_seen   TEXT,
    blocked     INTEGER DEFAULT 0
);
CREATE TABLE IF NOT EXISTS leads (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER,
    username    TEXT,
    name        TEXT,
    phone       TEXT,
    email       TEXT,
    service     TEXT,
    quiz_a      INTEGER,
    quiz_t      INTEGER,
    source      TEXT,
    lang        TEXT,
    created_at  TEXT
);
CREATE TABLE IF NOT EXISTS quiz (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER,
    a           INTEGER,
    t           INTEGER,
    created_at  TEXT
);
CREATE TABLE IF NOT EXISTS media (
    key         TEXT PRIMARY KEY,
    file_id     TEXT
);
"""


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class DB:
    def __init__(self, path: str):
        self.path = path
        self.conn: aiosqlite.Connection | None = None

    async def open(self):
        Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = await aiosqlite.connect(self.path)
        self.conn.row_factory = aiosqlite.Row
        await self.conn.executescript(SCHEMA)
        await self.conn.commit()

    async def close(self):
        if self.conn:
            await self.conn.close()

    # ── users ──
    async def touch_user(self, uid: int, username: str | None, full_name: str, source: str | None = None) -> bool:
        """Foydalanuvchini yozadi. Yangi bo'lsa True qaytaradi."""
        cur = await self.conn.execute("SELECT id FROM users WHERE id=?", (uid,))
        exists = await cur.fetchone()
        if exists:
            await self.conn.execute(
                "UPDATE users SET username=?, full_name=?, last_seen=?, blocked=0 WHERE id=?",
                (username, full_name, now(), uid))
        else:
            await self.conn.execute(
                "INSERT INTO users (id, username, full_name, source, created_at, last_seen) VALUES (?,?,?,?,?,?)",
                (uid, username, full_name, source, now(), now()))
        await self.conn.commit()
        return not exists

    async def get_lang(self, uid: int) -> str | None:
        cur = await self.conn.execute("SELECT lang FROM users WHERE id=?", (uid,))
        row = await cur.fetchone()
        return row["lang"] if row else None

    async def set_lang(self, uid: int, lang: str):
        await self.conn.execute("UPDATE users SET lang=? WHERE id=?", (lang, uid))
        await self.conn.commit()

    async def get_source(self, uid: int) -> str | None:
        cur = await self.conn.execute("SELECT source FROM users WHERE id=?", (uid,))
        row = await cur.fetchone()
        return row["source"] if row else None

    async def all_user_ids(self) -> list[int]:
        cur = await self.conn.execute("SELECT id FROM users WHERE blocked=0")
        return [r["id"] for r in await cur.fetchall()]

    async def mark_blocked(self, uid: int):
        await self.conn.execute("UPDATE users SET blocked=1 WHERE id=?", (uid,))
        await self.conn.commit()

    # ── quiz ──
    async def save_quiz(self, uid: int, a: int, t: int):
        await self.conn.execute("INSERT INTO quiz (user_id, a, t, created_at) VALUES (?,?,?,?)", (uid, a, t, now()))
        await self.conn.commit()

    async def last_quiz(self, uid: int) -> tuple[int, int] | None:
        cur = await self.conn.execute("SELECT a, t FROM quiz WHERE user_id=? ORDER BY id DESC LIMIT 1", (uid,))
        row = await cur.fetchone()
        return (row["a"], row["t"]) if row else None

    # ── leads ──
    async def add_lead(self, **kw) -> int:
        kw["created_at"] = now()
        cols = ", ".join(kw)
        q = ", ".join("?" for _ in kw)
        cur = await self.conn.execute(f"INSERT INTO leads ({cols}) VALUES ({q})", tuple(kw.values()))
        await self.conn.commit()
        return cur.lastrowid

    async def has_lead(self, uid: int) -> bool:
        cur = await self.conn.execute("SELECT 1 FROM leads WHERE user_id=? LIMIT 1", (uid,))
        return await cur.fetchone() is not None

    async def leads_csv(self) -> bytes:
        cur = await self.conn.execute("SELECT * FROM leads ORDER BY id")
        rows = await cur.fetchall()
        buf = io.StringIO()
        w = csv.writer(buf)
        if rows:
            w.writerow(rows[0].keys())
            for r in rows:
                w.writerow(list(r))
        else:
            w.writerow(["id", "user_id", "name", "phone", "email", "created_at"])
        return ("﻿" + buf.getvalue()).encode("utf-8")  # Excel uchun BOM

    async def stats(self) -> dict:
        async def one(q, *a):
            cur = await self.conn.execute(q, a)
            r = await cur.fetchone()
            return r[0] if r else 0
        today = datetime.now(timezone.utc).date().isoformat()
        return {
            "users": await one("SELECT COUNT(*) FROM users"),
            "active": await one("SELECT COUNT(*) FROM users WHERE blocked=0"),
            "users_today": await one("SELECT COUNT(*) FROM users WHERE created_at LIKE ?", today + "%"),
            "leads": await one("SELECT COUNT(*) FROM leads"),
            "leads_today": await one("SELECT COUNT(*) FROM leads WHERE created_at LIKE ?", today + "%"),
            "quiz": await one("SELECT COUNT(*) FROM quiz"),
            "quiz_a": round(await one("SELECT AVG(a) FROM quiz") or 0),
            "quiz_t": round(await one("SELECT AVG(t) FROM quiz") or 0),
            "langs": {r[0] or "—": r[1] for r in await (await self.conn.execute(
                "SELECT lang, COUNT(*) FROM users GROUP BY lang")).fetchall()},
            "sources": {r[0] or "—": r[1] for r in await (await self.conn.execute(
                "SELECT source, COUNT(*) FROM users GROUP BY source ORDER BY 2 DESC LIMIT 8")).fetchall()},
        }

    # ── media cache ──
    async def get_media(self, key: str) -> str | None:
        cur = await self.conn.execute("SELECT file_id FROM media WHERE key=?", (key,))
        row = await cur.fetchone()
        return row["file_id"] if row else None

    async def set_media(self, key: str, file_id: str):
        await self.conn.execute("INSERT OR REPLACE INTO media (key, file_id) VALUES (?,?)", (key, file_id))
        await self.conn.commit()


from config import cfg  # noqa: E402

db = DB(cfg.db_path)
