# Project Structure

The Exodia Assistant App is organized for clarity and modularity. Here's an overview:

```text
exodia-assistant-app/
├── README.md
├── DEVELOPMENT.md
├── docs/
├── src/
│   └── files/
│       └── exodia-assistant/
│           ├── app/
│           │   ├── core/
│           │   ├── roles/
│           │   ├── ui/
│           │   ├── utils/
│           ├── assets/
│           ├── config.py
│           ├── main.py
│           └── requirements.txt
```

## Directory and File Purpose

- **README.md**: Project summary and user-facing info.
- **DEVELOPMENT.md**: Developer notes (now points to `docs/`).
- **docs/**: Full documentation (you are here!).
- **src/**: All source code.
- **src/files/exodia-assistant/app/core/**: Core logic, settings, and role management.
- **src/files/exodia-assistant/app/roles/**: Role system and user profiles.
- **src/files/exodia-assistant/app/ui/**: UI components (windows, widgets, panels).
- **src/files/exodia-assistant/app/utils/**: Utility functions (file, font, HTML, etc.).
- **src/files/exodia-assistant/assets/**: Fonts, images, icons, and HTML content.
- **src/files/exodia-assistant/config.py**: App configuration.
- **src/files/exodia-assistant/main.py**: App entry point.
- **src/files/exodia-assistant/requirements.txt**: Python dependencies.

See `components.md` for a breakdown of each main component. 