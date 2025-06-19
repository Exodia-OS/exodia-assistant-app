# Development Environment Setup

## Prerequisites
- Python 3.6 or higher
- PyQt5
- PyYAML
- python-xlib

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Exodia-OS/exodia-apps.git
   cd exodia-apps/exodia-assistant-app
   ```
2. **Install system dependencies:**
   ```bash
   sudo pacman -S python-xlib exodia-pip-venv python-pyqt5
   ```
3. **Install Python dependencies:**
   ```bash
   cd src/files/exodia-assistant/
   pip install -r requirements.txt
   ```
4. **Run the application:**
   ```bash
   python main.py
   ```

## Troubleshooting
- If you see missing module errors, ensure all dependencies are installed.
- For display issues, check your PyQt5 installation and system theme.
- For font issues, verify the custom fonts are present in `assets/fonts/`.

## Notes
- The app is developed and tested on Linux (Arch-based). Other distros may require package name adjustments.
- Use a virtual environment for Python dependencies if possible.

See `contributing.md` for workflow and best practices. 