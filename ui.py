"""Ekranlar: har bir bo'lim = bitta kadr (rasm + caption + tugmalar).

Navigatsiya bitta xabarni tahrirlash orqali ishlaydi — chat "lenta"ga
aylanmaydi, foydalanuvchi bitta ekranda kadrma-kadr yuradi.
"""
from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass
from typing import Callable

from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters.callback_data import CallbackData
from aiogram.types import (BufferedInputFile, InlineKeyboardButton, InlineKeyboardMarkup,
                           InputMediaPhoto, Message, WebAppInfo)

import render
from config import cfg
from db import db
from texts import CASES, FOCUS, LANG_NAMES, LANGS, QUIZ_AXES, people, t

log = logging.getLogger(__name__)


# ───────────────────────── callback'lar ─────────────────────────

class Nav(CallbackData, prefix="n"):
    s: str          # ekran nomi
    i: int = 0      # indeks (keys, bosqich, qadam)


class Lang(CallbackData, prefix="lg"):
    code: str


class Quiz(CallbackData, prefix="q"):
    i: int          # savol indeksi (-1 = boshlash)
    v: int = 0      # ball: 2 / 1 / 0


class LeadCb(CallbackData, prefix="ld"):
    svc: str = ""   # a | b | quiz | case<n> | ""
    force: int = 0


class Noop(CallbackData, prefix="x"):
    pass


def btn(text: str, cb: CallbackData | None = None, url: str | None = None,
        web_app: str | None = None) -> InlineKeyboardButton:
    if web_app:
        return InlineKeyboardButton(text=text, web_app=WebAppInfo(url=web_app))
    if url:
        return InlineKeyboardButton(text=text, url=url)
    return InlineKeyboardButton(text=text, callback_data=(cb or Noop()).pack())


def kb(*rows: list[InlineKeyboardButton]) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[r for r in rows if r])


def home_row(lang: str, back: CallbackData | None = None) -> list[InlineKeyboardButton]:
    row = []
    if back:
        row.append(btn(t(lang, "b_back"), back))
    row.append(btn(t(lang, "b_home"), Nav(s="home")))
    return row


# ───────────────────────── ekran modeli ─────────────────────────

@dataclass
class Screen:
    key: str | None                     # kesh kaliti (None = har safar yangidan chiziladi)
    factory: Callable[[], bytes]        # rasm generatori
    caption: str
    markup: InlineKeyboardMarkup


def _k(*parts) -> str:
    return ":".join(str(p) for p in parts) + f":v{render.RENDER_VERSION}"


def scr_language() -> Screen:
    rows = [[btn(LANG_NAMES[c], Lang(code=c))] for c in LANGS]
    caption = t("uz", "choose_lang")
    return Screen(_k("lang"), render.card_language, caption, kb(*rows))


def scr_home(lang: str) -> Screen:
    L = lambda k: t(lang, k)  # noqa: E731
    last = [btn(L("b_lang"), Nav(s="lang"))]
    if cfg.site_url.startswith("https://"):
        last.append(btn(L("b_site"), web_app=cfg.site_url))
    markup = kb(
        [btn(L("b_about"), Nav(s="about")), btn(L("b_works"), Nav(s="works"))],
        [btn(L("b_services"), Nav(s="svc")), btn(L("b_journey"), Nav(s="jour", i=-1))],
        [btn(L("b_process"), Nav(s="proc")), btn(L("b_quiz"), Quiz(i=-1))],
        [btn(L("b_lead"), LeadCb())],
        last,
    )
    return Screen(_k("home", lang),
                  lambda: render.card_cover(L("name_lines"), L("role"), L("slate")),
                  L("home"), markup)


def scr_about(lang: str) -> Screen:
    L = lambda k: t(lang, k)  # noqa: E731
    links = [btn(n, url=u) for n, u in cfg.links]
    markup = kb(
        links,
        [btn(L("b_works"), Nav(s="works")), btn(L("b_lead"), LeadCb())],
        home_row(lang),
    )
    return Screen(_k("about", lang),
                  lambda: render.card_about(L("about_kicker"), L("about_head"), (L("chip_a"), L("chip_t"))),
                  L("about"), markup)


def case_caption(lang: str, i: int) -> str:
    L = lambda k: t(lang, k)  # noqa: E731
    c = CASES[i]
    task, concept = c["t"][lang]
    sc = L("sc")
    credits = "\n".join(
        f"• {L(role)}: {'<b>' if 'AB' in ids else ''}{people(ids, lang)}{'</b>' if 'AB' in ids else ''}"
        for role, ids in c["credits"])
    return (
        f"🎞 <b>{c['client']}</b>  ·  <code>SC {i + 1:02d}/{len(CASES):02d}</code>\n"
        f"<i>{'AB Media' if c['exec'] == 'AB Media' else 'AB Media × ' + c['exec']}</i>\n\n"
        f"🎯 <b>{L('l_task')}:</b> {task}\n\n"
        f"💡 <b>{L('l_concept')}:</b> {concept}\n\n"
        f"🎬 <b>{L('l_scope')}:</b> {' · '.join(sc[k] for k in c['scope'])}\n\n"
        f"👥 <b>{L('l_team')}:</b>\n{credits}"
    )


def scr_case(lang: str, i: int) -> Screen:
    n = len(CASES)
    i %= n
    c = CASES[i]
    markup = kb(
        [btn("◀️", Nav(s="works", i=(i - 1) % n)),
         btn(f"SC {i + 1:02d} / {n:02d}", Noop()),
         btn("▶️", Nav(s="works", i=(i + 1) % n))],
        [btn(t(lang, "b_want"), LeadCb(svc=f"case{i}"))],
        home_row(lang),
    )
    return Screen(_k("case", lang, i),
                  lambda: render.card_case(i, n, c["client"], c["t"][lang][1], c["exec"]),
                  case_caption(lang, i), markup)


def scr_services(lang: str) -> Screen:
    L = lambda k: t(lang, k)  # noqa: E731
    markup = kb(
        [btn(L("b_svc_a"), LeadCb(svc="a"))],
        [btn(L("b_svc_b"), LeadCb(svc="b"))],
        [btn(L("b_process"), Nav(s="proc"))],
        home_row(lang),
    )
    return Screen(_k("svc", lang),
                  lambda: render.card_services(L("svc_kicker"), (L("svc_a"), L("svc_a_items")),
                                               (L("svc_b"), L("svc_b_items"))),
                  L("svc"), markup)


def scr_journey(lang: str, i: int) -> Screen:
    L = lambda k: t(lang, k)  # noqa: E731
    st = L("st")
    active = None if i < 0 else i % len(st)

    def label(k: int) -> str:
        mark = "◉ " if k == active else ("🎯 " if k in FOCUS else "")
        return f"{mark}{st[k][0]}"

    markup = kb(
        [btn(label(k), Nav(s="jour", i=k)) for k in range(0, 3)],
        [btn(label(k), Nav(s="jour", i=k)) for k in range(3, len(st))],
        [btn(L("b_quiz"), Quiz(i=-1))],
        home_row(lang),
    )
    if active is None:
        caption = L("j_intro")
    else:
        name, desc = st[active]
        caption = f"🧭 <b>{active + 1:02d} · {name}</b>\n<i>{desc}</i>\n\n{L('j_stage_notes')[active]}"
        if active in FOCUS:
            caption += f"\n\n{L('j_mine')}"
    return Screen(_k("jour", lang, -1 if active is None else active),
                  lambda: render.card_journey(L("j_title"), st, FOCUS, L("j_focus"), active),
                  caption, markup)


def scr_process(lang: str, i: int) -> Screen:
    L = lambda k: t(lang, k)  # noqa: E731
    steps = L("steps")
    n = len(steps)
    i %= n
    bar = "▰" * (i + 1) + "▱" * (n - i - 1) + f"  00:{i * 12:02d}:{(i * 7) % 25:02d}"
    caption = L("p_cap").format(i=i + 1, n=n, h=steps[i][0], p=steps[i][1], bar=bar)
    nav = []
    if i > 0:
        nav.append(btn("◀️ " + steps[i - 1][0], Nav(s="proc", i=i - 1)))
    if i < n - 1:
        nav.append(btn(steps[i + 1][0] + " ▶️", Nav(s="proc", i=i + 1)))
    markup = kb(
        nav,
        [btn(L("b_lead"), LeadCb())] if i == n - 1 else [],
        home_row(lang),
    )
    return Screen(_k("proc", lang, i),
                  lambda: render.card_process(L("p_title"), steps, i), caption, markup)


def scr_quiz_intro(lang: str) -> Screen:
    L = lambda k: t(lang, k)  # noqa: E731
    return Screen(_k("take", lang, 0),
                  lambda: render.card_take(0, len(QUIZ_AXES), L("q_label")),
                  L("q_intro"),
                  kb([btn(L("b_q_start"), Quiz(i=0, v=-1))], home_row(lang)))


def scr_quiz_q(lang: str, i: int) -> Screen:
    L = lambda k: t(lang, k)  # noqa: E731
    n = len(QUIZ_AXES)
    yes, part, no = L("q_ans")
    markup = kb(
        [btn(yes, Quiz(i=i, v=2)), btn(part, Quiz(i=i, v=1)), btn(no, Quiz(i=i, v=0))],
        home_row(lang),
    )
    return Screen(_k("take", lang, i + 1),
                  lambda: render.card_take(i + 1, n, L("q_label")),
                  L("q_cap").format(i=i + 1, n=n, q=L("q")[i]), markup)


def verdict(a: int, tr: int) -> str:
    if a >= 67 and tr >= 67:
        return "strong"
    if a < 40 and tr < 40:
        return "both"
    return "aw" if a < tr else "tr"


def scr_quiz_result(lang: str, a: int, tr: int) -> Screen:
    L = lambda k: t(lang, k)  # noqa: E731
    title, text = L("r")[verdict(a, tr)]
    caption = L("r_cap").format(title=title, a=a, t=tr, text=text)
    markup = kb(
        [btn(L("b_q_lead"), LeadCb(svc="quiz"))],
        [btn(L("b_q_again"), Quiz(i=-1))],
        home_row(lang),
    )
    return Screen(None, lambda: render.card_result(L("r_a"), L("r_t"), a, tr, title, L("r_kicker")),
                  caption, markup)


def scr_lead_intro(lang: str) -> Screen:
    L = lambda k: t(lang, k)  # noqa: E731
    return Screen(_k("lead", lang),
                  lambda: render.card_slate_text(L("lead_kicker"), L("lead_big"), L("lead_sub"), False, "SC 06 · TK 01"),
                  L("lead_intro"), kb(home_row(lang)))


def scr_lead_done(lang: str, name: str) -> Screen:
    L = lambda k: t(lang, k)  # noqa: E731
    from html import escape
    return Screen(_k("done", lang),
                  lambda: render.card_slate_text("SC 06 · TK 01", L("done_big"), L("done_sub"), True, "CUT"),
                  L("done").format(n=escape(name)),
                  kb([btn(L("b_works"), Nav(s="works")), btn(L("b_quiz"), Quiz(i=-1))], home_row(lang)))


# ───────────────────────── ko'rsatish ─────────────────────────

async def _media(screen: Screen):
    if screen.key:
        fid = await db.get_media(screen.key)
        if fid:
            return fid, False
    data = await asyncio.to_thread(screen.factory)
    return BufferedInputFile(data, filename="frame.jpg"), True


async def show(bot: Bot, chat_id: int, screen: Screen, msg: Message | None = None) -> Message | None:
    """msg berilsa va u rasm bo'lsa — o'sha kadrni almashtiradi, aks holda yangisini yuboradi."""
    media, fresh = await _media(screen)
    sent = None
    if msg is not None and msg.photo:
        try:
            sent = await msg.edit_media(
                InputMediaPhoto(media=media, caption=screen.caption, parse_mode=ParseMode.HTML),
                reply_markup=screen.markup)
        except TelegramBadRequest as e:
            if "not modified" in str(e):
                return msg
            log.info("edit_media failed (%s) — sending new frame", e)
            if fresh:  # yuklangan fayl obyektini qayta ishlatib bo'lmaydi
                media, fresh = await _media(screen)
            sent = None
    if not isinstance(sent, Message):
        sent = await bot.send_photo(chat_id, media, caption=screen.caption, reply_markup=screen.markup)
    if fresh and screen.key and isinstance(sent, Message) and sent.photo:
        await db.set_media(screen.key, sent.photo[-1].file_id)
    return sent
