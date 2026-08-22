#!/usr/bin/env python3

import sys
import os
import subprocess
import importlib.util

if importlib.util.find_spec("PyQt6") is None:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "PyQt6"])

import json
import time
import random
import urllib.request
import urllib.parse
import urllib.error
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
    QPushButton, QLabel, QScrollArea, QCheckBox, QFrame, QMessageBox,
    QTabWidget, QComboBox, QGridLayout, QGraphicsDropShadowEffect,
    QTextEdit, QInputDialog, QListView, QDialog
)
from PyQt6.QtGui import QPixmap, QImage, QFont, QColor, QKeySequence, QShortcut, QTextCursor
from PyQt6.QtCore import (
    Qt, QThread, pyqtSignal, QRunnable, QThreadPool, QObject, QPoint,
    QPropertyAnimation, QEasingCurve
)
from PyQt6.QtNetwork import QLocalServer, QLocalSocket

# ---------------------------------------------------------------------------
# Локализация / Translations
# ---------------------------------------------------------------------------
LANGS = {
    "RU": {
        "pin_off": "📌 Поверх окон",
        "pin_on": "📌 Открепить",
        "debug": "🐞 Debug",
        "tab_player": "👤 Аватар игрока",
        "tab_catalog": "🛒 Поиск в каталоге",
        "input_nick_ph": "Введи Roblox Nick...",
        "btn_fetch": "🔍 Загрузить",
        "avatar_placeholder": "Введите ник",
        "notes_placeholder": "Заметки...",
        "btn_swap": "🎲 Заменить Offsale",
        "saved_outfits": "💾 Сохранённые сеты:",
        "btn_load_set": "📂 Загрузить",
        "btn_save_set": "💾 Сохранить",
        "btn_copy_all": "📋 СКОПИРОВАТЬ ВЕСЬ СЕТ",
        "status_ready": "Готов к работе",
        "input_catalog_ph": "Поиск вещей в каталоге...",
        "cat_types": ["Рубашки", "Штаны", "Шляпы/Аксессуары", "Волосы"],
        "btn_search": "🔍 Найти",
        "btn_copy": "📋 Копировать",
        "btn_open_page": "🌐 Открыть страницу",
        "btn_add_player": "➕ Добавить игроку",
        "btn_del": "🗑 Удалить",
        "chip_catalog": "В каталоге",
        "chip_offsale": "Offsale",
        "chip_avail": "Доступно",
        "chip_swapped": "SWAPPED",
        "err_title": "Ошибка",
        "empty_set": "Текущий сет пуст!",
        "save_title": "Сохранить сет",
        "save_prompt": "Введите имя сета:",
        "info_title": "Информация",
        "success_title": "Успех",
        "empty_title": "Пусто",
        "no_selection": "Не выбрано ни одной вещи!",
        "debug_title": "🐞 Debug — сетевые запросы",
        "debug_pause": "⏸ Пауза",
        "debug_resume": "▶ Продолжить",
        "debug_clear": "🗑 Очистить",
        "debug_waiting": "Ожидание запросов…",
    },
    "EN": {
        "pin_off": "📌 Always on Top",
        "pin_on": "📌 Unpin Window",
        "debug": "🐞 Debug",
        "tab_player": "👤 Player Avatar",
        "tab_catalog": "🛒 Catalog Search",
        "input_nick_ph": "Enter Roblox Username...",
        "btn_fetch": "🔍 Load",
        "avatar_placeholder": "Enter Username",
        "notes_placeholder": "Notes...",
        "btn_swap": "🎲 Swap Offsale",
        "saved_outfits": "💾 Saved Outfits:",
        "btn_load_set": "📂 Load",
        "btn_save_set": "💾 Save",
        "btn_copy_all": "📋 COPY FULL OUTFIT",
        "status_ready": "Ready",
        "input_catalog_ph": "Search catalog items...",
        "cat_types": ["Shirts", "Pants", "Hats/Accessories", "Hair"],
        "btn_search": "🔍 Search",
        "btn_copy": "📋 Copy",
        "btn_open_page": "🌐 Open Page",
        "btn_add_player": "➕ Add to Player",
        "btn_del": "🗑 Delete",
        "chip_catalog": "In Catalog",
        "chip_offsale": "Offsale",
        "chip_avail": "Available",
        "chip_swapped": "SWAPPED",
        "err_title": "Error",
        "empty_set": "Current outfit is empty!",
        "save_title": "Save Outfit",
        "save_prompt": "Enter outfit name:",
        "info_title": "Information",
        "success_title": "Success",
        "empty_title": "Empty",
        "no_selection": "No items selected!",
        "debug_title": "🐞 Debug — Network Requests",
        "debug_pause": "⏸ Pause",
        "debug_resume": "▶ Resume",
        "debug_clear": "🗑 Clear",
        "debug_waiting": "Waiting for requests…",
    }
}

FAVORITE_SHIRTS = ["5319900634", "6070624075", "6829585000"]
FAVORITE_PANTS = ["5319909330", "6070625000"]

# ---------------------------------------------------------------------------
# Палитра — берётся из themes.json (тема "dark" по умолчанию), можно
# переключить на "light" или добавить свою тему в файл вручную/через диалог.
# ---------------------------------------------------------------------------
THEMES_FILE = Path(__file__).resolve().parent / "themes.json"

DEFAULT_THEMES = {
    "dark": {
        "BG": "#0d0d0d", "SURFACE": "#161616", "SURFACE_ALT": "#1f1f1f",
        "BORDER": "#2c2c2c", "ACCENT": "#f5f5f5", "ACCENT_HOVER": "#ffffff",
        "GREEN": "#3ecf8e", "RED": "#ff4d4d", "ORANGE": "#f5f5f5",
        "TEXT": "#f5f5f5", "TEXT_DIM": "#8a8a8a", "ON_ACCENT": "#0d0d0d",
    },
    "light": {
        "BG": "#f5f5f5", "SURFACE": "#ffffff", "SURFACE_ALT": "#ececec",
        "BORDER": "#dcdcdc", "ACCENT": "#0d0d0d", "ACCENT_HOVER": "#2a2a2a",
        "GREEN": "#0d0d0d", "RED": "#d63333", "ORANGE": "#0d0d0d",
        "TEXT": "#0d0d0d", "TEXT_DIM": "#6b6b6b", "ON_ACCENT": "#f5f5f5",
    },
}


def load_themes() -> dict:
    if THEMES_FILE.exists():
        try:
            with open(THEMES_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                merged = dict(DEFAULT_THEMES)
                merged.update(data)
                return merged
        except Exception:
            pass
    return dict(DEFAULT_THEMES)


def save_themes(themes: dict):
    with open(THEMES_FILE, "w", encoding="utf-8") as f:
        json.dump(themes, f, ensure_ascii=False, indent=2)


ACTIVE_THEME_FILE = Path(__file__).resolve().parent / "active_theme.json"


def load_active_theme_name() -> str:
    if ACTIVE_THEME_FILE.exists():
        try:
            with open(ACTIVE_THEME_FILE, "r", encoding="utf-8") as f:
                return json.load(f).get("theme", "dark")
        except Exception:
            pass
    return "dark"


def save_active_theme_name(name: str):
    with open(ACTIVE_THEME_FILE, "w", encoding="utf-8") as f:
        json.dump({"theme": name}, f)


_THEMES = load_themes()
_ACTIVE_THEME_NAME = load_active_theme_name()
_ACTIVE = _THEMES.get(_ACTIVE_THEME_NAME, _THEMES["dark"])

BG = _ACTIVE["BG"]
SURFACE = _ACTIVE["SURFACE"]
SURFACE_ALT = _ACTIVE["SURFACE_ALT"]
BORDER = _ACTIVE["BORDER"]
ACCENT = _ACTIVE["ACCENT"]
ACCENT_HOVER = _ACTIVE["ACCENT_HOVER"]
GREEN = _ACTIVE["GREEN"]
RED = _ACTIVE["RED"]
ORANGE = _ACTIVE["ORANGE"]
TEXT = _ACTIVE["TEXT"]
TEXT_DIM = _ACTIVE["TEXT_DIM"]
ON_ACCENT = _ACTIVE.get("ON_ACCENT", "#0d0d0d")

ICON_DISPLAY_SIZE = 84
ICON_SIZE_MIN = 48
ICON_SIZE_MAX = 160
ICON_SIZE_STEP = 12
AVATAR_DISPLAY_SIZE = 220
MAX_PARALLEL_LOADS = 6

ICON_CACHE: dict[str, QPixmap] = {}
SCRIPT_DIR = Path(__file__).resolve().parent
OUTFITS_FILE = SCRIPT_DIR / "outfits.json"
SINGLE_INSTANCE_KEY = "town-outfit-builder-r6-singleinstance"


class SingleInstanceGuard:
    def __init__(self, key=SINGLE_INSTANCE_KEY):
        self.key = key
        self.server = None
        self._on_activate_requested = None

    def try_acquire(self, on_activate_requested) -> bool:
        self._on_activate_requested = on_activate_requested

        probe = QLocalSocket()
        probe.connectToServer(self.key)
        if probe.waitForConnected(200):
            probe.write(b"activate")
            probe.flush()
            probe.waitForBytesWritten(200)
            probe.disconnectFromServer()
            return False

        # Кроссплатформенная очистка сокета/канала перед стартом
        self.server = QLocalServer()
        if sys.platform != "win32":
            QLocalServer.removeServer(self.key)
            
        self.server.newConnection.connect(self._handle_new_connection)
        
        # Если порт всё ещё занят на Windows (бывает при крашах) — перезаписываем
        if not self.server.listen(self.key):
            if sys.platform == "win32":
                QLocalServer.removeServer(self.key)
                self.server.listen(self.key)

        return True

    def _handle_new_connection(self):
        conn = self.server.nextPendingConnection()
        if conn is None:
            return
        conn.readyRead.connect(lambda: self._read_activate(conn))

    def _read_activate(self, conn):
        data = bytes(conn.readAll())
        conn.disconnectFromServer()
        if data == b"activate" and self._on_activate_requested:
            self._on_activate_requested()


def load_outfits() -> dict:
    if not OUTFITS_FILE.exists():
        return {}
    try:
        with open(OUTFITS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_outfits(outfits: dict):
    with open(OUTFITS_FILE, "w", encoding="utf-8") as f:
        json.dump(outfits, f, ensure_ascii=False, indent=2)


class DebugLog(QObject):
    event = pyqtSignal(str, str, str)
    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = DebugLog()
        return cls._instance

    def log(self, level, title, detail=""):
        self.event.emit(level, title, detail)


def _short(text, limit=400):
    text = str(text)
    return text if len(text) <= limit else text[:limit] + " …"


def fetch_json(url, method="GET", data=None, extra_headers=None):
    log = DebugLog.instance()
    headers = {"User-Agent": "Mozilla/5.0"}
    if extra_headers:
        headers.update(extra_headers)

    log.log("info", f"→ {method} {url}", "")
    t0 = time.monotonic()
    try:
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        with urllib.request.urlopen(req, timeout=15) as res:
            raw = res.read().decode()
            elapsed = (time.monotonic() - t0) * 1000
            log.log("ok", f"← {res.status} {url}", f"{elapsed:.0f}ms  {_short(raw)}")
            return json.loads(raw)
    except urllib.error.HTTPError as e:
        body = ""
        try:
            body = e.read().decode()
        except Exception:
            pass
        elapsed = (time.monotonic() - t0) * 1000
        log.log("err", f"✕ {e.code} {url}", f"{elapsed:.0f}ms  {_short(body or e.reason)}")
        raise
    except Exception as e:
        elapsed = (time.monotonic() - t0) * 1000
        log.log("err", f"✕ EXCEPTION {url}", f"{elapsed:.0f}ms  {_short(e)}")
        raise


class FetchWorker(QThread):
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)

    def __init__(self, username):
        super().__init__()
        self.username = username

    def run(self):
        try:
            u_data = fetch_json(
                "https://users.roblox.com/v1/usernames/users",
                method="POST",
                data=json.dumps({"usernames": [self.username]}).encode(),
                extra_headers={"Content-Type": "application/json"}
            )
            if not u_data.get("data"):
                self.error.emit(f"User '{self.username}' not found!")
                return
            user_id = u_data["data"][0]["id"]

            avatar_url = f"https://thumbnails.roblox.com/v1/users/avatar?userIds={user_id}&size=352x352&format=Png&isCircular=false"
            avatar_img_url = fetch_json(avatar_url)["data"][0]["imageUrl"]

            w_url = f"https://avatar.roblox.com/v1/users/{user_id}/currently-wearing"
            asset_ids = fetch_json(w_url).get("assetIds", [])

            items = []
            icon_ids = []
            for aid in asset_ids:
                try:
                    d = fetch_json(f"https://economy.roblox.com/v2/assets/{aid}/details")
                    t = d.get("AssetTypeId")
                    if t not in [11, 12, 8, 41, 42, 43, 44, 45, 46, 47]:
                        continue
                    is_unavail = not d.get("IsForSale", False) or d.get("IsLimited", False) or d.get("IsLimitedUnique", False)
                    items.append({
                        "id": str(aid),
                        "name": d.get("Name", "Item"),
                        "type": t,
                        "is_unavail": is_unavail,
                        "icon": ""
                    })
                    icon_ids.append(str(aid))
                except Exception:
                    continue

            if icon_ids:
                try:
                    icon_data = fetch_json(
                        f"https://thumbnails.roblox.com/v1/assets?assetIds={','.join(icon_ids)}&size=150x150&format=Png"
                    )
                    icon_map = {str(d["targetId"]): d["imageUrl"] for d in icon_data.get("data", [])}
                    for it in items:
                        it["icon"] = icon_map.get(it["id"], "")
                except Exception:
                    pass

            self.finished.emit({
                "username": self.username,
                "user_id": user_id,
                "avatar_img": avatar_img_url,
                "items": items
            })
        except Exception as e:
            self.error.emit(str(e))


CATALOG_CATEGORY_MAPPING = {
    0: (3, 56),
    1: (3, 57),
    2: (11, None),
    3: (None, None),
}

CATALOG_TYPE_MAPPING = {
    0: [11],
    1: [12],
    2: [8, 42, 43, 44, 45, 46, 47],
    3: [41],
}

CATALOG_SEARCH_LIMIT = 30
CATALOG_SORT_RELEVANCE = 0
CATALOG_API_BASE = "https://catalog.roblox.com"
LAYERED_NAME_MARKERS = ("layered", "layer", "3d pants", "3d shirt")


def looks_layered(name: str) -> bool:
    low = name.lower()
    return any(marker in low for marker in LAYERED_NAME_MARKERS)


class WikiPageLoader(QThread):
    loaded = pyqtSignal(str)

    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        import re
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                              "(KHTML, like Gecko) Chrome/124.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
            }
            req = urllib.request.Request(self.url, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as res:
                html = res.read().decode("utf-8", errors="ignore")
            m = re.search(r'<div class="mw-parser-output">(.*?)<div class="printfooter"', html, re.S)
            content = m.group(1) if m else html
            content = re.sub(r'<script.*?</script>', '', content, flags=re.S)
            content = re.sub(r'<style.*?</style>', '', content, flags=re.S)
            content = re.sub(r'<[^>]+>', ' ', content)
            content = content.replace('&nbsp;', ' ').replace('&amp;', '&')
            content = re.sub(r'\s*\n\s*', '\n', content)
            content = re.sub(r'[ \t]{2,}', ' ', content)
            content = re.sub(r'\n{3,}', '\n\n', content).strip()
            self.loaded.emit(content[:8000] if content else "No content extracted.")
        except Exception as e:
            self.loaded.emit(f"Failed to load page: {e}\n\nUse 'Open in browser' instead.")


class CatalogWorker(QThread):
    finished = pyqtSignal(list)
    error = pyqtSignal(str)

    def __init__(self, query, filter_type):
        super().__init__()
        self.query = query
        self.filter_type = filter_type

    def _keyword_only_url(self):
        params = urllib.parse.urlencode({
            "Keyword": self.query,
            "Limit": CATALOG_SEARCH_LIMIT,
            "SortType": CATALOG_SORT_RELEVANCE,
        })
        return f"{CATALOG_API_BASE}/v1/search/items/details?{params}"

    def run(self):
        try:
            allowed_types = CATALOG_TYPE_MAPPING.get(self.filter_type, [])
            category, subcategory = CATALOG_CATEGORY_MAPPING.get(self.filter_type, (None, None))

            data = None
            if category is not None:
                try:
                    precise_params = {
                        "Keyword": self.query,
                        "Category": category,
                        "Limit": CATALOG_SEARCH_LIMIT,
                        "SortType": CATALOG_SORT_RELEVANCE,
                    }
                    if subcategory is not None:
                        precise_params["Subcategory"] = subcategory
                    url = f"{CATALOG_API_BASE}/v1/search/items/details?{urllib.parse.urlencode(precise_params)}"
                    data = fetch_json(url)
                except urllib.error.HTTPError:
                    data = None

            if data is None:
                data = fetch_json(self._keyword_only_url())

            items, asset_ids = [], []
            for item in data.get("data", []):
                if item.get("itemType") == "Asset":
                    t = item.get("assetType", 0)
                    if allowed_types and t not in allowed_types:
                        continue
                    name = item.get("name", "Item")
                    if looks_layered(name):
                        continue
                    items.append({
                        "id": str(item["id"]),
                        "name": name,
                        "type": t
                    })
                    asset_ids.append(str(item["id"]))

            if not asset_ids:
                self.finished.emit([])
                return

            icon_data = fetch_json(
                f"https://thumbnails.roblox.com/v1/assets?assetIds={','.join(asset_ids)}&size=150x150&format=Png"
            )
            icon_map = {str(d["targetId"]): d["imageUrl"] for d in icon_data.get("data", [])}
            for item in items:
                item["icon"] = icon_map.get(item["id"], "")

            self.finished.emit(items)
        except Exception as e:
            self.error.emit(str(e))


class ImageLoadSignals(QObject):
    loaded = pyqtSignal(object, object)


class ImageLoadTask(QRunnable):
    def __init__(self, url, target_ref, display_size):
        super().__init__()
        self.url = url
        self.target_ref = target_ref
        self.display_size = display_size
        self.signals = ImageLoadSignals()

    def run(self):
        try:
            cache_key = f"{self.url}@{self.display_size}"
            cached = ICON_CACHE.get(cache_key)
            if cached is not None:
                self.signals.loaded.emit(self.target_ref, cached)
                return

            req = urllib.request.Request(self.url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=15) as res:
                raw = res.read()

            img = QImage()
            img.loadFromData(raw)
            pix = QPixmap.fromImage(img).scaled(
                self.display_size, self.display_size,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            ICON_CACHE[cache_key] = pix
            self.signals.loaded.emit(self.target_ref, pix)
        except Exception:
            pass


class LoaderPool:
    _pool = None

    @classmethod
    def get(cls):
        if cls._pool is None:
            cls._pool = QThreadPool()
            cls._pool.setMaxThreadCount(MAX_PARALLEL_LOADS)
        return cls._pool


def load_icon_async(url, label: QLabel, size: int):
    if not url:
        return
    task = ImageLoadTask(url, label, size)

    def _apply(target_label, pixmap):
        try:
            if target_label is not None:
                target_label.setPixmap(pixmap)
        except RuntimeError:
            pass

    task.signals.loaded.connect(_apply)
    LoaderPool.get().start(task)


LEVEL_COLOR = {"info": TEXT_DIM, "ok": GREEN, "err": RED}
LEVEL_ICON = {"info": "→", "ok": "✓", "err": "✕"}
MAX_LOG_LINES = 400


class DebugPanel(QWidget):
    PANEL_WIDTH = 380

    def __init__(self, parent=None, lang="RU"):
        super().__init__(None, Qt.WindowType.Window)
        self.setWindowTitle("Debug")
        self.resize(560, 500)
        self.lang = lang
        self._line_count = 0
        self._paused = False
        self.setStyleSheet(f"QWidget {{ background: {SURFACE}; color: {TEXT}; }}")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 12, 14, 14)
        layout.setSpacing(8)

        header = QHBoxLayout()
        self.title = QLabel(LANGS[self.lang]["debug_title"])
        self.title.setFont(QFont("Sans", 11, QFont.Weight.Bold))
        self.title.setStyleSheet(f"color: {TEXT};")
        header.addWidget(self.title)
        header.addStretch()

        self.btn_pause = ghost_button(LANGS[self.lang]["debug_pause"])
        self.btn_pause.setFixedWidth(100)
        self.btn_pause.clicked.connect(self.toggle_pause)
        header.addWidget(self.btn_pause)

        self.btn_clear = ghost_button(LANGS[self.lang]["debug_clear"])
        self.btn_clear.setFixedWidth(100)
        self.btn_clear.clicked.connect(self.clear_log)
        header.addWidget(self.btn_clear)

        btn_close = ghost_button("✕")
        btn_close.setFixedWidth(36)
        btn_close.clicked.connect(lambda: self.window().toggle_debug_panel())
        header.addWidget(btn_close)

        layout.addLayout(header)

        self.log_view = QTextEdit()
        self.log_view.setReadOnly(True)
        self.log_view.setStyleSheet(f"""
            QTextEdit {{
                background: {BG};
                color: {TEXT};
                border: 1px solid {BORDER};
                border-radius: 20px;
                padding: 8px;
                font-family: 'JetBrains Mono', 'Consolas', monospace;
                font-size: 11px;
            }}
        """)
        layout.addWidget(self.log_view, 1)

        self.status_label = QLabel(LANGS[self.lang]["debug_waiting"])
        self.status_label.setStyleSheet(f"color: {TEXT_DIM}; font-size: 10px;")
        layout.addWidget(self.status_label)

        DebugLog.instance().event.connect(self.append_event)

    def set_language(self, lang):
        self.lang = lang
        self.title.setText(LANGS[self.lang]["debug_title"])
        self.btn_pause.setText(LANGS[self.lang]["debug_resume"] if self._paused else LANGS[self.lang]["debug_pause"])
        self.btn_clear.setText(LANGS[self.lang]["debug_clear"])

    def toggle_pause(self):
        self._paused = not self._paused
        self.btn_pause.setText(LANGS[self.lang]["debug_resume"] if self._paused else LANGS[self.lang]["debug_pause"])

    def clear_log(self):
        self.log_view.clear()
        self._line_count = 0
        self.status_label.setText(LANGS[self.lang]["debug_clear"])

    def append_event(self, level, title, detail):
        if self._paused:
            return
        color = LEVEL_COLOR.get(level, TEXT)
        icon = LEVEL_ICON.get(level, "•")
        ts = time.strftime("%H:%M:%S")

        html = f'<div style="margin-bottom:6px;">'
        html += f'<span style="color:{TEXT_DIM};">[{ts}]</span> '
        html += f'<span style="color:{color}; font-weight:600;">{icon} {title}</span>'
        if detail:
            html += f'<br><span style="color:{TEXT_DIM};">{detail}</span>'
        html += '</div>'

        self.log_view.append(html)
        self._line_count += 1

        if self._line_count > MAX_LOG_LINES:
            cursor = self.log_view.textCursor()
            cursor.movePosition(QTextCursor.MoveOperation.Start)
            for _ in range(50):
                cursor.select(QTextCursor.SelectionType.BlockUnderCursor)
                cursor.removeSelectedText()
                cursor.deleteChar()
            self._line_count -= 50

        self.log_view.moveCursor(QTextCursor.MoveOperation.End)
        self.status_label.setText(f"Events: {self._line_count}")


def make_shadow(blur=20, alpha=90, y=4):
    eff = QGraphicsDropShadowEffect()
    eff.setBlurRadius(blur)
    eff.setOffset(0, y)
    eff.setColor(QColor(0, 0, 0, alpha))
    return eff


def primary_button(text):
    btn = QPushButton(text)
    btn.setCursor(Qt.CursorShape.PointingHandCursor)
    btn.setStyleSheet(f"""
        QPushButton {{
            padding: 10px 16px;
            background: {ACCENT};
            color: {ON_ACCENT};
            font-weight: 600;
            border-radius: 20px;
            border: none;
        }}
        QPushButton:hover {{ background: {ACCENT_HOVER}; }}
        QPushButton:pressed {{ background: #cccccc; }}
    """)
    return btn


def ghost_button(text, color=TEXT_DIM):
    btn = QPushButton(text)
    btn.setCursor(Qt.CursorShape.PointingHandCursor)
    btn.setStyleSheet(f"""
        QPushButton {{
            padding: 8px 14px;
            background: transparent;
            color: {color};
            font-weight: 600;
            border-radius: 20px;
            border: 1px solid {BORDER};
        }}
        QPushButton:hover {{ background: {SURFACE_ALT}; color: {TEXT}; }}
    """)
    return btn


def line_edit(placeholder):
    le = QLineEdit()
    le.setPlaceholderText(placeholder)
    le.setStyleSheet(f"""
        QLineEdit {{
            padding: 10px 12px;
            background: {SURFACE};
            color: {TEXT};
            border: 1px solid {BORDER};
            border-radius: 20px;
            font-size: 13px;
            selection-background-color: {ACCENT};
            selection-color: {ON_ACCENT};
        }}
        QLineEdit:focus {{ border: 1px solid {ACCENT}; }}
    """)
    return le


def styled_combo():
    cb = QComboBox()
    cb.setCursor(Qt.CursorShape.PointingHandCursor)
    view = QListView()
    view.setSpacing(2)
    view.setUniformItemSizes(True)
    view.setAlternatingRowColors(False)
    view.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
    view.setStyleSheet(f"""
        QListView {{
            background: {SURFACE};
            color: {TEXT};
            border: 1px solid {BORDER};
            border-radius: 20px;
            outline: none;
            padding: 4px;
        }}
        QListView::item {{
            min-height: 28px;
            padding: 4px 10px;
            border: none;
        }}
        QListView::item:hover {{ background: {SURFACE_ALT}; }}
        QListView::item:selected {{ background: {ACCENT}; color: {ON_ACCENT}; }}
    """)
    cb.setView(view)

    _orig_show_popup = cb.showPopup
    def _show_popup():
        popup = cb.view().window()
        popup.setWindowFlags(
            Qt.WindowType.Popup | Qt.WindowType.FramelessWindowHint | Qt.WindowType.NoDropShadowWindowHint
        )
        popup.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        popup.setStyleSheet(f"background: {SURFACE}; border-radius: 20px;")
        _orig_show_popup()
    cb.showPopup = _show_popup
    cb.setStyleSheet(f"""
        QComboBox {{
            padding: 9px 14px;
            background: {SURFACE};
            color: {TEXT};
            border: 1px solid {BORDER};
            border-radius: 20px;
            font-weight: 600;
            font-size: 13px;
        }}
        QComboBox:hover {{ border: 1px solid {ACCENT}; }}
        QComboBox::drop-down {{
            border: none;
            width: 26px;
        }}
        QComboBox::down-arrow {{
            width: 10px;
            height: 10px;
        }}
        QComboBox QAbstractItemView {{
            background: {SURFACE};
            border: 1px solid {BORDER};
            border-radius: 20px;
            outline: none;
        }}
    """)
    return cb


class ItemCard(QFrame):
    def __init__(self, item, parent=None, is_catalog=False, on_add_to_player=None, on_delete=None, lang="RU"):
        super().__init__(parent)
        self.item = item
        self.is_catalog = is_catalog
        self.on_add_to_player = on_add_to_player
        self.on_delete = on_delete
        self.lang = lang

        self.setFixedWidth(180)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {SURFACE};
                border: 1px solid {BORDER};
                border-radius: 16px;
            }}
        """)
        self.setGraphicsEffect(make_shadow(blur=16, alpha=60, y=2))

        outer = QVBoxLayout(self)
        outer.setContentsMargins(10, 10, 10, 10)
        outer.setSpacing(8)

        top_row = QHBoxLayout()
        top_row.setSpacing(4)
        if not is_catalog:
            self.checkbox = QCheckBox()
            self.checkbox.setChecked(True)
            self.checkbox.setStyleSheet("QCheckBox::indicator { width: 16px; height: 16px; }")
            top_row.addWidget(self.checkbox)
        top_row.addStretch()
        outer.addLayout(top_row)

        self.img_label = QLabel()
        self.img_label.setFixedSize(ICON_DISPLAY_SIZE, ICON_DISPLAY_SIZE)
        self.img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.img_label.setStyleSheet(f"background: {SURFACE_ALT}; border-radius: 20px;")
        img_row = QHBoxLayout()
        img_row.addStretch()
        img_row.addWidget(self.img_label)
        img_row.addStretch()
        outer.addLayout(img_row)

        name_txt = item['name'][:22] + "…" if len(item['name']) > 22 else item['name']
        self.name_label = QLabel(name_txt)
        self.name_label.setFont(QFont("Sans", 10, QFont.Weight.Bold))
        self.name_label.setStyleSheet(f"color: {TEXT};")
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.name_label.setWordWrap(True)
        outer.addWidget(self.name_label)

        id_label = QLabel(f"ID {item['id']}")
        id_label.setStyleSheet(f"color: {TEXT_DIM}; font-size: 10px;")
        id_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        outer.addWidget(id_label)

        status = LANGS[self.lang]["chip_catalog"] if is_catalog else (LANGS[self.lang]["chip_offsale"] if item.get('is_unavail') else LANGS[self.lang]["chip_avail"])
        chip_color = GREEN if (is_catalog or not item.get('is_unavail')) else RED
        self.status_label = QLabel(status)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet(f"""
            color: {chip_color};
            background: {chip_color}22;
            border-radius: 16px;
            padding: 2px 8px;
            font-size: 10px;
            font-weight: 600;
        """)
        chip_row = QHBoxLayout()
        chip_row.addStretch()
        chip_row.addWidget(self.status_label)
        chip_row.addStretch()
        outer.addLayout(chip_row)

        self.btn_copy = ghost_button(LANGS[self.lang]["btn_copy"], color=ACCENT)
        self.btn_copy.clicked.connect(self.copy_single)
        outer.addWidget(self.btn_copy)

        id_row = QHBoxLayout()
        id_row.setSpacing(4)
        self.btn_copy_id = ghost_button("📋 ID", color=TEXT_DIM)
        self.btn_copy_id.clicked.connect(self.copy_id)
        id_row.addWidget(self.btn_copy_id)

        self.btn_open = ghost_button(LANGS[self.lang]["btn_open_page"], color=TEXT_DIM)
        self.btn_open.clicked.connect(self.open_item)
        id_row.addWidget(self.btn_open)
        outer.addLayout(id_row)

        if is_catalog and on_add_to_player is not None:
            self.btn_action = QPushButton(LANGS[self.lang]["btn_add_player"])
            self.btn_action.setCursor(Qt.CursorShape.PointingHandCursor)
            self.btn_action.setStyleSheet(f"""
                QPushButton {{
                    padding: 8px; background: {GREEN}; color: {ON_ACCENT};
                    font-weight: 700; border-radius: 20px; border: none; font-size: 11px;
                }}
                QPushButton:hover {{ background: #4fe0a0; }}
            """)
            self.btn_action.clicked.connect(lambda: self.on_add_to_player(dict(self.item)))
            outer.addWidget(self.btn_action)
        elif not is_catalog and on_delete is not None:
            self.btn_action = ghost_button(LANGS[self.lang]["btn_del"], color=RED)
            self.btn_action.clicked.connect(lambda: self.on_delete(self))
            outer.addWidget(self.btn_action)

        self.load_icon()

    def update_language(self, new_lang):
        self.lang = new_lang
        self.btn_copy.setText(LANGS[self.lang]["btn_copy"])
        self.btn_open.setText(LANGS[self.lang]["btn_open_page"])
        if hasattr(self, 'btn_action'):
            if self.is_catalog:
                self.btn_action.setText(LANGS[self.lang]["btn_add_player"])
            else:
                self.btn_action.setText(LANGS[self.lang]["btn_del"])
        
        if self.is_catalog:
            self.status_label.setText(LANGS[self.lang]["chip_catalog"])
        elif self.item.get('is_unavail'):
            self.status_label.setText(LANGS[self.lang]["chip_offsale"])
        else:
            self.status_label.setText(LANGS[self.lang]["chip_avail"])

    def copy_single(self):
        t = self.item['type']
        cmd = f"!hat {self.item['id']}"
        if t == 11:
            cmd = f"!shirt {self.item['id']}"
        elif t == 12:
            cmd = f"!pants {self.item['id']}"
        QApplication.clipboard().setText(cmd)

    def copy_id(self):
        QApplication.clipboard().setText(str(self.item['id']))

    def open_item(self):
        import webbrowser
        webbrowser.open(f"https://www.roblox.com/catalog/{self.item['id']}")

    def update_status(self):
        status = LANGS[self.lang]["chip_offsale"] if self.item.get('is_unavail') else LANGS[self.lang]["chip_swapped"]
        chip_color = RED if self.item.get('is_unavail') else GREEN
        self.status_label.setText(status)
        self.status_label.setStyleSheet(f"""
            color: {chip_color};
            background: {chip_color}22;
            border-radius: 16px;
            padding: 2px 8px;
            font-size: 10px;
            font-weight: 600;
        """)

    def load_icon(self):
        if not self.item.get('icon'):
            return
        load_icon_async(self.item['icon'], self.img_label, ICON_DISPLAY_SIZE)

    def resize_icon(self):
        self.img_label.setFixedSize(ICON_DISPLAY_SIZE, ICON_DISPLAY_SIZE)
        self.load_icon()


class TownOutfitBuilder(QWidget):
    BASE_WIDTH = 960
    BASE_HEIGHT = 700

    def __init__(self):
        super().__init__()
        self.lang = "EN"
        self.card_widgets = []
        self.current_user_id = None
        self.cat_card_widgets = []
        self.on_top = False
        self.debug_open = False
        self.debug_panel = DebugPanel(self, lang=self.lang)
        self.initUI()
        self._setup_shortcuts()
        self.refresh_outfits_combo()

        self._width_anim = QPropertyAnimation(self, b"size")
        self._width_anim.setDuration(240)
        self._width_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

    def closeEvent(self, event):
        # Исправлено безопасное закрытие для Windows/Qt
        super().closeEvent(event)

    def initUI(self):
        self.setWindowTitle("Town Outfit Builder (R6)")
        self.resize(1040, 700)
        self.setStyleSheet(f"""
            QWidget {{ background-color: {BG}; color: {TEXT}; font-family: 'Segoe UI', Sans; }}
            QScrollArea {{ border: none; background: transparent; }}
            QMessageBox {{ background-color: {SURFACE}; }}
        """)

        root_layout = QHBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # -- Боковая панель слева -------------------------------------
        sidebar = QFrame()
        sidebar.setFixedWidth(64)
        sidebar.setStyleSheet(f"background: {SURFACE}; border-right: 1px solid {BORDER};")
        side_layout = QVBoxLayout(sidebar)
        side_layout.setContentsMargins(8, 16, 8, 16)
        side_layout.setSpacing(10)
        side_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        def side_btn(emoji, tooltip, handler):
            b = QPushButton(emoji)
            b.setFixedSize(48, 48)
            b.setToolTip(tooltip)
            b.setCursor(Qt.CursorShape.PointingHandCursor)
            b.setStyleSheet(f"""
                QPushButton {{
                    background: {SURFACE_ALT}; color: {TEXT};
                    border: 1px solid {BORDER}; border-radius: 24px; font-size: 18px;
                }}
                QPushButton:hover {{ background: {ACCENT}; color: {ON_ACCENT}; }}
            """)
            b.clicked.connect(handler)
            return b

        self.side_player_btn = side_btn("👤", LANGS[self.lang]["tab_player"], lambda: self.tabs.setCurrentIndex(0))
        self.side_catalog_btn = side_btn("🛒", LANGS[self.lang]["tab_catalog"], lambda: self.tabs.setCurrentIndex(1))
        side_layout.addWidget(self.side_player_btn)
        side_layout.addWidget(self.side_catalog_btn)
        side_layout.addStretch()

        self.side_pin_btn = side_btn("📌", LANGS[self.lang]["pin_off"], self.toggle_always_on_top)
        self.side_debug_btn = side_btn("🐞", LANGS[self.lang]["debug"], self.toggle_debug_panel)
        self.side_zoom_in_btn = side_btn("+", "Icon size +", lambda: self.change_icon_size(ICON_SIZE_STEP))
        self.side_zoom_out_btn = side_btn("−", "Icon size -", lambda: self.change_icon_size(-ICON_SIZE_STEP))
        self.side_theme_btn = side_btn("🎨", "Theme", self.open_theme_dialog)
        self.side_wiring_btn = side_btn("⚡", "Wiring Wiki", self.open_wiring_wiki)
        side_layout.addWidget(self.side_pin_btn)
        side_layout.addWidget(self.side_wiring_btn)
        side_layout.addWidget(self.side_debug_btn)
        side_layout.addWidget(self.side_zoom_in_btn)
        side_layout.addWidget(self.side_zoom_out_btn)
        side_layout.addWidget(self.side_theme_btn)

        root_layout.addWidget(sidebar)

        # -- Правая часть: заголовок + контент -------------------------
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(16, 12, 16, 12)
        main_layout.setSpacing(10)

        top_bar = QHBoxLayout()
        top_bar.setSpacing(8)

        app_title = QLabel("👕 Town Outfit Builder")
        app_title.setFont(QFont("Sans", 13, QFont.Weight.Bold))
        app_title.setStyleSheet(f"color: {TEXT};")
        top_bar.addWidget(app_title)
        top_bar.addStretch()

        self.combo_lang = styled_combo()
        self.combo_lang.addItems(["RU", "EN"])
        self.combo_lang.setCurrentIndex(1)
        self.combo_lang.currentIndexChanged.connect(self.change_language)
        top_bar.addWidget(self.combo_lang)

        main_layout.addLayout(top_bar)

        body_layout = QHBoxLayout()
        body_layout.setSpacing(10)

        self.notes_edit = QTextEdit()
        self.notes_edit.setPlaceholderText(LANGS[self.lang]["notes_placeholder"])
        self.notes_edit.setFixedWidth(220)
        self.notes_edit.setStyleSheet(f"""
            QTextEdit {{
                background: {SURFACE}; color: {TEXT};
                border: 1px solid {BORDER}; border-radius: 20px;
                padding: 8px; font-size: 12px;
                selection-background-color: {ACCENT};
                selection-color: {ON_ACCENT};
            }}
        """)
        body_layout.addWidget(self.notes_edit)

        self.tabs = QTabWidget()
        self.tabs.tabBar().setVisible(False)
        self.tabs.setStyleSheet("QTabWidget::pane { border: none; }")

        self.tab_player = QWidget()
        self.setup_player_tab()
        self.tabs.addTab(self.tab_player, LANGS[self.lang]["tab_player"])

        self.tab_catalog = QWidget()
        self.setup_catalog_tab()
        self.tabs.addTab(self.tab_catalog, LANGS[self.lang]["tab_catalog"])

        body_layout.addWidget(self.tabs, 1)
        main_layout.addLayout(body_layout, 1)

        self.status_bar = QLabel(LANGS[self.lang]["status_ready"])
        self.status_bar.setStyleSheet(f"""
            color: {TEXT_DIM};
            font-size: 11px;
            padding: 6px 10px;
            background: {SURFACE};
            border-radius: 16px;
        """)
        main_layout.addWidget(self.status_bar)

        root_layout.addLayout(main_layout, 1)

    def change_language(self, index):
        self.lang = "RU" if index == 0 else "EN"
        self.debug_panel.set_language(self.lang)

        self.side_player_btn.setToolTip(LANGS[self.lang]["tab_player"])
        self.side_catalog_btn.setToolTip(LANGS[self.lang]["tab_catalog"])
        self.notes_edit.setPlaceholderText(LANGS[self.lang]["notes_placeholder"])
        self.btn_open_profile.setText(LANGS[self.lang]["btn_open_page"])
        self.side_pin_btn.setToolTip(LANGS[self.lang]["pin_on"] if self.on_top else LANGS[self.lang]["pin_off"])
        self.side_debug_btn.setToolTip(LANGS[self.lang]["debug"])
        self.tabs.setTabText(0, LANGS[self.lang]["tab_player"])
        self.tabs.setTabText(1, LANGS[self.lang]["tab_catalog"])

        self.input_nick.setPlaceholderText(LANGS[self.lang]["input_nick_ph"])
        self.btn_fetch.setText(LANGS[self.lang]["btn_fetch"])
        if self.avatar_label.text() in ["Введите ник", "Enter Username"]:
            self.avatar_label.setText(LANGS[self.lang]["avatar_placeholder"])
        self.btn_swap.setText(LANGS[self.lang]["btn_swap"])
        self.saves_label.setText(LANGS[self.lang]["saved_outfits"])
        self.btn_load_set.setText(LANGS[self.lang]["btn_load_set"])
        self.btn_save_set.setText(LANGS[self.lang]["btn_save_set"])
        self.btn_copy_all.setText(LANGS[self.lang]["btn_copy_all"])

        self.input_search.setPlaceholderText(LANGS[self.lang]["input_catalog_ph"])
        curr_cat = self.combo_type.currentIndex()
        self.combo_type.clear()
        self.combo_type.addItems(LANGS[self.lang]["cat_types"])
        self.combo_type.setCurrentIndex(curr_cat)
        self.btn_search.setText(LANGS[self.lang]["btn_search"])

        for card in self.card_widgets:
            card.update_language(self.lang)
        for card in self.cat_card_widgets:
            card.update_language(self.lang)

        self.set_status(LANGS[self.lang]["status_ready"])

    def _setup_shortcuts(self):
        QShortcut(QKeySequence(Qt.Key.Key_Escape), self, activated=self.close)
        QShortcut(QKeySequence("Ctrl+D"), self, activated=self.toggle_debug_panel)
        QShortcut(QKeySequence("Ctrl+T"), self, activated=self.toggle_always_on_top)

    def toggle_always_on_top(self):
        self.on_top = not self.on_top
        flags = self.windowFlags()
        if self.on_top:
            flags |= Qt.WindowType.WindowStaysOnTopHint
            self.side_pin_btn.setToolTip(LANGS[self.lang]["pin_on"])
            self.side_pin_btn.setStyleSheet(f"""
                QPushButton {{
                    background: {ACCENT}; color: {ON_ACCENT};
                    border: 1px solid {BORDER}; border-radius: 18px; font-size: 18px;
                }}
            """)
        else:
            flags &= ~Qt.WindowType.WindowStaysOnTopHint
            self.side_pin_btn.setToolTip(LANGS[self.lang]["pin_off"])
            self.side_pin_btn.setStyleSheet(f"""
                QPushButton {{
                    background: {SURFACE_ALT}; color: {TEXT};
                    border: 1px solid {BORDER}; border-radius: 18px; font-size: 18px;
                }}
                QPushButton:hover {{ background: {ACCENT}; color: {ON_ACCENT}; }}
            """)
        self.setWindowFlags(flags)
        self.show()

    def toggle_debug_panel(self):
        if self.debug_panel.isVisible():
            self.debug_panel.hide()
        else:
            self.debug_panel.show()
            self.debug_panel.raise_()
            self.debug_panel.activateWindow()

    def set_status(self, text):
        self.status_bar.setText(text)

    # -- Player tab ---------------------------------------------------------
    def setup_player_tab(self):
        layout = QVBoxLayout(self.tab_player)
        layout.setSpacing(12)

        top_layout = QHBoxLayout()
        top_layout.setSpacing(8)
        self.input_nick = line_edit(LANGS[self.lang]["input_nick_ph"])
        self.input_nick.returnPressed.connect(self.start_fetch)

        self.btn_fetch = primary_button(LANGS[self.lang]["btn_fetch"])
        self.btn_fetch.clicked.connect(self.start_fetch)

        top_layout.addWidget(self.input_nick, 1)
        top_layout.addWidget(self.btn_fetch)
        layout.addLayout(top_layout)

        content_layout = QHBoxLayout()
        content_layout.setSpacing(16)

        left_box = QVBoxLayout()
        left_box.setSpacing(10)

        avatar_frame = QFrame()
        avatar_frame.setFixedSize(AVATAR_DISPLAY_SIZE + 20, AVATAR_DISPLAY_SIZE + 20)
        avatar_frame.setStyleSheet(f"background: {SURFACE}; border-radius: 20px; border: 1px solid {BORDER};")
        avatar_frame.setGraphicsEffect(make_shadow())
        af_layout = QVBoxLayout(avatar_frame)
        self.avatar_label = QLabel(LANGS[self.lang]["avatar_placeholder"])
        self.avatar_label.setFixedSize(AVATAR_DISPLAY_SIZE, AVATAR_DISPLAY_SIZE)
        self.avatar_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.avatar_label.setStyleSheet(f"color: {TEXT_DIM}; background: transparent;")
        af_layout.addWidget(self.avatar_label)
        left_box.addWidget(avatar_frame)

        profile_row = QHBoxLayout()
        profile_row.setSpacing(4)
        self.btn_copy_uid = ghost_button("📋 ID", color=TEXT_DIM)
        self.btn_copy_uid.clicked.connect(self.copy_player_id)
        profile_row.addWidget(self.btn_copy_uid)
        self.btn_open_profile = ghost_button(LANGS[self.lang]["btn_open_page"], color=TEXT_DIM)
        self.btn_open_profile.clicked.connect(self.open_player_profile)
        profile_row.addWidget(self.btn_open_profile)
        left_box.addLayout(profile_row)

        self.btn_swap = QPushButton(LANGS[self.lang]["btn_swap"])
        self.btn_swap.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_swap.setStyleSheet(f"""
            QPushButton {{
                padding: 10px; background: {ORANGE}; color: {ON_ACCENT};
                font-weight: 700; border-radius: 20px; border: none;
            }}
            QPushButton:hover {{ background: #f0b357; }}
        """)
        self.btn_swap.clicked.connect(self.swap_offsale)
        left_box.addWidget(self.btn_swap)

        saves_box = QVBoxLayout()
        saves_box.setSpacing(6)
        self.saves_label = QLabel(LANGS[self.lang]["saved_outfits"])
        self.saves_label.setStyleSheet(f"color: {TEXT_DIM}; font-size: 11px; font-weight: 600;")
        saves_box.addWidget(self.saves_label)

        self.combo_outfits = styled_combo()
        saves_box.addWidget(self.combo_outfits)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(6)

        self.btn_load_set = ghost_button(LANGS[self.lang]["btn_load_set"], color=TEXT)
        self.btn_load_set.clicked.connect(self.load_selected_outfit)
        btn_row.addWidget(self.btn_load_set)

        self.btn_save_set = ghost_button(LANGS[self.lang]["btn_save_set"], color=GREEN)
        self.btn_save_set.clicked.connect(self.save_current_outfit)
        btn_row.addWidget(self.btn_save_set)

        btn_del_set = ghost_button("🗑", color=RED)
        btn_del_set.setFixedWidth(36)
        btn_del_set.clicked.connect(self.delete_selected_outfit)
        btn_row.addWidget(btn_del_set)

        saves_box.addLayout(btn_row)
        left_box.addLayout(saves_box)
        left_box.addStretch()

        content_layout.addLayout(left_box)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.items_layout = QGridLayout(self.scroll_content)
        self.items_layout.setSpacing(12)
        self.items_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.scroll.setWidget(self.scroll_content)

        content_layout.addWidget(self.scroll, 1)
        layout.addLayout(content_layout, 1)

        self.btn_copy_all = QPushButton(LANGS[self.lang]["btn_copy_all"])
        self.btn_copy_all.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_copy_all.setStyleSheet(f"""
            QPushButton {{
                padding: 13px; background: {GREEN}; color: {ON_ACCENT};
                font-weight: 700; border-radius: 20px; border: none; font-size: 13px;
            }}
            QPushButton:hover {{ background: #4fe0a0; }}
        """)
        self.btn_copy_all.clicked.connect(self.copy_full_outfit)
        layout.addWidget(self.btn_copy_all)

    # -- Catalog tab ----------------------------------------------------------
    def setup_catalog_tab(self):
        layout = QVBoxLayout(self.tab_catalog)
        layout.setSpacing(12)

        top_layout = QHBoxLayout()
        top_layout.setSpacing(8)

        self.input_search = line_edit(LANGS[self.lang]["input_catalog_ph"])
        self.input_search.returnPressed.connect(self.search_catalog)

        self.combo_type = styled_combo()
        self.combo_type.addItems(LANGS[self.lang]["cat_types"])
        self.combo_type.setMinimumWidth(160)

        self.btn_search = primary_button(LANGS[self.lang]["btn_search"])
        self.btn_search.clicked.connect(self.search_catalog)

        top_layout.addWidget(self.input_search, 1)
        top_layout.addWidget(self.combo_type)
        top_layout.addWidget(self.btn_search)
        layout.addLayout(top_layout)

        self.cat_scroll = QScrollArea()
        self.cat_scroll.setWidgetResizable(True)
        self.cat_scroll_content = QWidget()
        self.cat_items_layout = QGridLayout(self.cat_scroll_content)
        self.cat_items_layout.setSpacing(12)
        self.cat_items_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.cat_scroll.setWidget(self.cat_scroll_content)
        layout.addWidget(self.cat_scroll, 1)

    # -- helpers --------------------------------------------------------------
    def _clear_grid(self, grid_layout, widget_list=None):
        while grid_layout.count():
            item = grid_layout.takeAt(0)
            w = item.widget()
            if w:
                w.setParent(None)
                w.deleteLater()
        if widget_list is not None:
            widget_list.clear()

    def _grid_columns(self, scroll_area, card_width=180 + 12):
        width = max(scroll_area.viewport().width(), card_width)
        return max(1, width // card_width)

    def regrid_player_items(self):
        while self.items_layout.count():
            item = self.items_layout.takeAt(0)
            w = item.widget()
            if w:
                w.setParent(None)

        cols = self._grid_columns(self.scroll)
        for i, card in enumerate(self.card_widgets):
            row, col = divmod(i, cols)
            self.items_layout.addWidget(card, row, col)

    def remove_player_item(self, card_widget):
        if card_widget in self.card_widgets:
            item_name = card_widget.item.get('name', 'Item')
            self.card_widgets.remove(card_widget)
            card_widget.deleteLater()
            self.regrid_player_items()
            msg = f"Item «{item_name}» removed" if self.lang == "EN" else f"Вещь «{item_name}» удалена"
            self.set_status(msg)

    # -- Saves logic ----------------------------------------------------------
    def refresh_outfits_combo(self):
        self.combo_outfits.clear()
        outfits = load_outfits()
        if outfits:
            self.combo_outfits.addItems(list(outfits.keys()))

    def save_current_outfit(self):
        if not self.card_widgets:
            QMessageBox.warning(self, LANGS[self.lang]["err_title"], LANGS[self.lang]["empty_set"])
            return
        name, ok = QInputDialog.getText(self, LANGS[self.lang]["save_title"], LANGS[self.lang]["save_prompt"])
        if ok and name.strip():
            name = name.strip()
            outfits = load_outfits()
            outfits[name] = [card.item for card in self.card_widgets if card.checkbox.isChecked()]
            save_outfits(outfits)
            self.refresh_outfits_combo()
            self.combo_outfits.setCurrentText(name)
            msg = f"Outfit «{name}» saved!" if self.lang == "EN" else f"Сет «{name}» сохранён!"
            self.set_status(msg)

    def load_selected_outfit(self):
        name = self.combo_outfits.currentText()
        if not name:
            return
        outfits = load_outfits()
        items = outfits.get(name, [])
        if not items:
            return
        self._clear_grid(self.items_layout, self.card_widgets)
        cols = self._grid_columns(self.scroll)
        for i, item in enumerate(items):
            card = ItemCard(item, on_delete=self.remove_player_item, lang=self.lang)
            row, col = divmod(i, cols)
            self.items_layout.addWidget(card, row, col)
            self.card_widgets.append(card)
        msg = f"Loaded outfit «{name}» ({len(items)} items)" if self.lang == "EN" else f"Загружен сет «{name}» ({len(items)} предметов)"
        self.set_status(msg)

    def delete_selected_outfit(self):
        name = self.combo_outfits.currentText()
        if not name:
            return
        outfits = load_outfits()
        if name in outfits:
            del outfits[name]
            save_outfits(outfits)
            self.refresh_outfits_combo()
            msg = f"Outfit «{name}» deleted" if self.lang == "EN" else f"Сет «{name}» удалён"
            self.set_status(msg)

    # -- Player logic -----------------------------------------------------
    def add_item_to_player(self, item):
        if any(card.item['id'] == item['id'] for card in self.card_widgets):
            msg = f"Item ID {item['id']} is already in set" if self.lang == "EN" else f"Предмет ID {item['id']} уже есть в вашем сете"
            self.set_status(msg)
            return
        card = ItemCard(dict(item), on_delete=self.remove_player_item, lang=self.lang)
        cols = self._grid_columns(self.scroll)
        idx = len(self.card_widgets)
        row, col = divmod(idx, cols)
        self.items_layout.addWidget(card, row, col)
        self.card_widgets.append(card)
        msg = f"«{item['name']}» added to outfit" if self.lang == "EN" else f"«{item['name']}» добавлен в текущий сет"
        self.set_status(msg)

    def change_icon_size(self, delta):
        global ICON_DISPLAY_SIZE
        new_size = max(ICON_SIZE_MIN, min(ICON_SIZE_MAX, ICON_DISPLAY_SIZE + delta))
        if new_size == ICON_DISPLAY_SIZE:
            return
        ICON_DISPLAY_SIZE = new_size
        for card in self.card_widgets:
            card.resize_icon()
        for card in self.cat_card_widgets:
            card.resize_icon()

    def open_wiring_wiki(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("Wiring — Roblox Town Wiki")
        dlg.resize(640, 560)
        dlg.setStyleSheet(f"QDialog {{ background: {SURFACE}; }}")
        layout = QVBoxLayout(dlg)

        view = QTextEdit()
        view.setReadOnly(True)
        view.setStyleSheet(f"""
            QTextEdit {{
                background: {BG}; color: {TEXT}; border: 1px solid {BORDER};
                border-radius: 16px; padding: 12px; font-size: 13px;
            }}
        """)
        view.setText("Loading…")
        layout.addWidget(view)

        btn_row = QHBoxLayout()
        btn_browser = ghost_button("🌐 Open in browser", color=TEXT_DIM)
        btn_browser.clicked.connect(lambda: __import__("webbrowser").open("https://roblox-town.fandom.com/wiki/Wiring"))
        btn_row.addWidget(btn_browser)
        btn_row.addStretch()
        btn_close = primary_button("Close")
        btn_close.clicked.connect(dlg.close)
        btn_row.addWidget(btn_close)
        layout.addLayout(btn_row)

        loader = WikiPageLoader("https://roblox-town.fandom.com/wiki/Wiring")
        loader.loaded.connect(view.setText)
        loader.start()
        dlg._loader = loader

        dlg.exec()

    def open_theme_dialog(self):
        themes = load_themes()
        names = list(themes.keys())
        current = load_active_theme_name()
        idx = names.index(current) if current in names else 0
        choice, ok = QInputDialog.getItem(
            self, "Theme", "Select theme:", names, idx, False
        )
        if ok and choice and choice != current:
            save_active_theme_name(choice)
            os.execv(sys.executable, [sys.executable] + sys.argv)

    def copy_player_id(self):
        if self.current_user_id:
            QApplication.clipboard().setText(str(self.current_user_id))

    def open_player_profile(self):
        if self.current_user_id:
            import webbrowser
            webbrowser.open(f"https://www.roblox.com/users/{self.current_user_id}/profile")

    def start_fetch(self):
        nick = self.input_nick.text().strip()
        if not nick:
            return
        self.avatar_label.setText("Loading..." if self.lang == "EN" else "Загрузка...")
        self.avatar_label.setPixmap(QPixmap())
        self._clear_grid(self.items_layout, self.card_widgets)
        msg = f"Searching player «{nick}»…" if self.lang == "EN" else f"Ищу игрока «{nick}»…"
        self.set_status(msg)

        self.worker = FetchWorker(nick)
        self.worker.finished.connect(self.on_data_loaded)
        self.worker.error.connect(self._on_fetch_error)
        self.worker.start()

    def _on_fetch_error(self, e):
        self.set_status(f"Error: {e}")
        QMessageBox.critical(self, LANGS[self.lang]["err_title"], e)

    def on_data_loaded(self, data):
        self.current_user_id = data.get("user_id")
        load_icon_async(data["avatar_img"], self.avatar_label, AVATAR_DISPLAY_SIZE)

        cols = self._grid_columns(self.scroll)
        for i, item in enumerate(data["items"]):
            card = ItemCard(item, on_delete=self.remove_player_item, lang=self.lang)
            row, col = divmod(i, cols)
            self.items_layout.addWidget(card, row, col)
            self.card_widgets.append(card)

        offsale = sum(1 for it in data["items"] if it.get("is_unavail"))
        msg = (
            f"{data['username']}: found {len(data['items'])} items, offsale: {offsale}"
            if self.lang == "EN" else
            f"{data['username']}: найдено {len(data['items'])} предметов, из них offsale: {offsale}"
        )
        self.set_status(msg)

    def swap_offsale(self):
        swapped = 0
        for card in self.card_widgets:
            if card.item.get('is_unavail') and card.checkbox.isChecked():
                t = card.item['type']
                if t == 11:
                    card.item['id'] = random.choice(FAVORITE_SHIRTS)
                    card.item['name'] = "[RANDOM] Base Shirt"
                    card.item['is_unavail'] = False
                    card.update_status()
                    swapped += 1
                elif t == 12:
                    card.item['id'] = random.choice(FAVORITE_PANTS)
                    card.item['name'] = "[RANDOM] Base Pants"
                    card.item['is_unavail'] = False
                    card.update_status()
                    swapped += 1
        if swapped > 0:
            msg = f"Replaced {swapped} offsale items!" if self.lang == "EN" else f"Заменено {swapped} оффсейл вещей!"
            QMessageBox.information(self, LANGS[self.lang]["info_title"], msg)

    def copy_full_outfit(self):
        normal_cmds, unavail_cmds = [], []
        for card in self.card_widgets:
            if not card.checkbox.isChecked():
                continue
            item = card.item
            t = item['type']
            cmd = None
            if t == 11:
                cmd = f"!shirt {item['id']}"
            elif t == 12:
                cmd = f"!pants {item['id']}"
            elif t in [8, 41, 42, 43, 44, 45, 46, 47]:
                cmd = f"!hat {item['id']}"

            if cmd:
                if item.get('is_unavail'):
                    unavail_cmds.append(cmd)
                else:
                    normal_cmds.append(cmd)

        all_cmds = normal_cmds + unavail_cmds
        if not all_cmds:
            QMessageBox.warning(self, LANGS[self.lang]["empty_title"], LANGS[self.lang]["no_selection"])
            return
        QApplication.clipboard().setText(" | ".join(all_cmds))
        
        status_msg = f"Copied {len(all_cmds)} commands" if self.lang == "EN" else f"Скопировано {len(all_cmds)} команд в буфер обмена"
        box_msg = "Full outfit copied! Press Ctrl+V in chat." if self.lang == "EN" else "Весь сет скопирован! Нажимай Ctrl+V в чате."
        
        self.set_status(status_msg)
        QMessageBox.information(self, LANGS[self.lang]["success_title"], box_msg)

    # -- Catalog logic ------------------------------------------------------
    def search_catalog(self):
        query = self.input_search.text().strip()
        if not query:
            return

        self._clear_grid(self.cat_items_layout, self.cat_card_widgets)
        msg = f"Searching catalog «{query}»…" if self.lang == "EN" else f"Ищу в каталоге «{query}»…"
        self.set_status(msg)

        filter_type = self.combo_type.currentIndex()
        self.cat_worker = CatalogWorker(query, filter_type)
        self.cat_worker.finished.connect(self.on_catalog_loaded)
        self.cat_worker.error.connect(self._on_fetch_error)
        self.cat_worker.start()

    def on_catalog_loaded(self, items):
        if not items:
            msg_not_found = "Nothing found for this query." if self.lang == "EN" else "Ничего не найдено по этому запросу."
            self.set_status(msg_not_found)
            QMessageBox.information(self, LANGS[self.lang]["empty_title"], msg_not_found)
            return

        cols = self._grid_columns(self.cat_scroll)
        for i, item in enumerate(items):
            card = ItemCard(item, is_catalog=True, on_add_to_player=self.add_item_to_player, lang=self.lang)
            row, col = divmod(i, cols)
            self.cat_items_layout.addWidget(card, row, col)
            self.cat_card_widgets.append(card)

        msg_found = f"Found {len(items)} items" if self.lang == "EN" else f"Найдено {len(items)} предметов"
        self.set_status(msg_found)


if __name__ == "__main__":
    if not THEMES_FILE.exists():
        save_themes(DEFAULT_THEMES)

    app = QApplication(sys.argv)

    guard = SingleInstanceGuard()
    window = TownOutfitBuilder()

    def on_activate():
        window.show()
        window.raise_()
        window.activateWindow()

    if not guard.try_acquire(on_activate):
        sys.exit(0)

    window.show()
    sys.exit(app.exec())
