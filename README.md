# MIMICRIA

<p align="left">
  <img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/PyQt-6-41CD52?style=for-the-badge&logo=qt&logoColor=white" alt="PyQt6">
  <img src="https://img.shields.io/badge/License-GPLv3-blue?style=for-the-badge" alt="License">
</p>

**English** | [Русский](#русский)

---

## English

**MIMICRIA** is a Python application designed to inspect Roblox avatar profiles, extract equipped asset IDs, and generate executable commands to mimic their outfit in-game. It only calls the official `roblox.com` and `rbxcdn.com` APIs.

Works on both **Windows** and **Linux**. Source is fully readable in a single file — check `Mimicria[0.3].py` yourself before running it, as with any script you download from the internet.

### Features
* **Avatar Inspection:** Fetch equipped items from any user by username.
* **Command Generation:** Builds ready-to-use in-game wear commands.
* **GUI:** Interface built with PyQt6.
* **Themes:** Dark/Light built-in, custom themes via `themes.json`.
* **Cross-Platform:** Windows and Linux.

### Installation & Setup

**1. Install Python**
Python 3.8+ is required.
- **Windows:** download from [python.org](https://www.python.org/downloads/) — check **"Add python.exe to PATH"** during install.
- **Linux:** usually preinstalled. If not: `sudo apt install python3 python3-pip` (Debian/Ubuntu).

**2. Get the files**
Download `Mimicria[0.3].py`, `themes.json`, and `requirements.txt` from this repo into the same folder (**Code → Download ZIP**, or individually).

**3. Install dependencies**

It's recommended to use a virtual environment so this doesn't touch your system Python packages:
```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Without a venv:
```bash
pip install -r requirements.txt --break-system-packages   # Linux only, if pip refuses otherwise
```

**4. Run**
```bash
python3 "Mimicria[0.3].py"      # Windows: py "Mimicria[0.3].py"
```

The app does not auto-install anything on its own — dependencies are only installed by the commands above, which you run yourself.

---

## Русский

**MIMICRIA** — приложение на Python для анализа профилей аватаров Roblox: извлекает ID надетых предметов и генерирует готовые команды, чтобы повторить чужой образ прямо в игре. Обращается только к официальным API `roblox.com` и `rbxcdn.com`.

Работает на **Windows** и **Linux**. Весь код в одном файле — перед запуском можешь сам открыть `Mimicria[0.3].py` и проверить, что в нём, как и с любым скриптом из интернета.

### Возможности
* **Анализ аватара:** список надетых вещей по никнейму.
* **Генерация команд:** готовые команды для надевания в игре.
* **GUI:** интерфейс на PyQt6.
* **Темы:** встроенные Dark/Light, кастомные темы через `themes.json`.
* **Кроссплатформенность:** Windows и Linux.

### Установка и запуск

**1. Установите Python**
Нужен Python 3.8+.
- **Windows:** [python.org](https://www.python.org/downloads/) — при установке поставьте галочку **"Add python.exe to PATH"**.
- **Linux:** обычно уже есть. Если нет: `sudo apt install python3 python3-pip` (Debian/Ubuntu).

**2. Скачайте файлы**
Скачайте `Mimicria[0.3].py`, `themes.json` и `requirements.txt` в одну папку (**Code → Download ZIP** или по отдельности).

**3. Установите зависимости**

Рекомендуется через виртуальное окружение, чтобы не трогать системные пакеты:
```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Без venv:
```bash
pip install -r requirements.txt --break-system-packages   # только Linux, если pip иначе отказывается
```

**4. Запуск**
```bash
python3 "Mimicria[0.3].py"      # Windows: py "Mimicria[0.3].py"
```

Приложение ничего не устанавливает само — зависимости ставятся только командами выше, которые запускаешь ты сам.
