# Exodia Assistant App Documentation

Welcome to the Exodia Assistant App documentation! This guide will help you understand, set up, and contribute to the project with ease.

## What is Exodia Assistant?
Exodia Assistant is a comprehensive helper application for Exodia OS, providing users with system information, documentation, keybindings, news, and more—all in a modern, custom-shaped interface built with Python and PyQt5.

## Key Features
- Welcome screen and onboarding
- News updates from Exodia OS
- Keybinding reference (searchable)
- Wiki and knowledge base
- System tweaks and configuration
- Role-based user profiles (tools now configured in TOML files)
- Developer information
- Custom UI/UX

## Quick Start

### Prerequisites
- Python 3.6+
- PyQt5
- toml
- python-xlib

### Setup
```bash
git clone https://github.com/Exodia-OS/exodia-apps.git
cd exodia-apps/exodia-assistant-app
sudo pacman -S python-xlib exodia-pip-venv python-pyqt5
cd src/files/exodia-assistant/
pip install -r requirements.txt
```

### Run the App
```bash
python main.py
```

---

For detailed guides, see the other docs in this directory. 