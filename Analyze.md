# Exodia Assistant Application Analysis

## Overview
Exodia Assistant is a comprehensive desktop application for Exodia OS, providing users with a modern, custom-shaped interface to access system information, documentation, keybindings, news, role-based environments, and more. The app is built with PyQt5 and is highly modular, supporting extensibility through roles and configuration files.

---

## Architecture & Main Components

- **Entry Point**: `main.py`
  - Launches the PyQt5 application and the main custom-shaped window (`CustomShapeWindow`).

- **Configuration**: `config.py`
  - Centralizes all global constants, directory paths, and environment settings (e.g., asset locations, user config, WM_CLASS, app version).

- **UI Layer**: `app/ui/`
  - **windows/**: Main and internal window classes, custom shapes, and window management.
  - **widgets/**: Custom widgets (profile picture, side button panel, etc.).
  - **tabs/**: Content tabs (wiki, tweaks, news, role UI, etc.).
  - **keybinding/**: Keybinding reference UI.

- **Core Logic**: `app/core/`
  - **role.py**: Role management, loading, and display logic.
  - **role_env_setup.py**: Environment setup for roles, including tool install/uninstall, dependency management, and UI for tool configuration.
  - **settings.py**: Settings window, YAML-based settings management, backup/restore, and validation.

- **Utilities**: `app/utils/`
  - Helper modules for fonts, HTML, file operations, X11 integration, UI utilities, and role utilities (e.g., YAML role selection, role directory management).

- **Roles System**: `app/roles/`
  - **profiles/**: Contains directories for each role (DevOps, Backend, Frontend, MLOps), each with its own `tools.yaml`, `materials.html`, `roadmap.html`, and assets.
  - **role.yaml**: Stores the currently selected role.

- **Assets**: `assets/`
  - Fonts, icons, images, HTML templates, and other static resources.

---

## UI & Navigation
- **Custom Window Shape**: The main window uses a polygonal mask for a unique look.
- **Side Button Panel**: Navigation is handled by a custom widget with large, stylized buttons for each main section (Welcome, News, Keybinding, Wiki, Tweaks, Role, Developers).
- **Profile Picture**: Circular, user-configurable, loaded from settings or fallback.
- **Internal Window**: Displays the main content area, switching between tabs and role-specific content.

---

## Role Management & Environment Setup
- **Role Selection**: Users can select, create, or manage roles. Roles are stored as directories under `profiles/`.
- **Role Content**: Each role can have its own HTML/Markdown for materials, roadmap, and a YAML file for tool definitions.
- **Environment Setup**: 
  - Tools and dependencies are defined in `tools.yaml` per role.
  - The UI allows batch install/uninstall, shows tooltips with dependency info, and uses `pacman`/`paru` for package management.
  - Pre/post install/remove scripts are supported for advanced setup.

---

## Settings & Configuration
- **YAML-based Settings**: All user settings (theme, font size, auto-start, profile picture, etc.) are stored in `settings.yaml`.
- **Robustness**: Settings are validated, with backup/restore logic to recover from corruption.
- **Profile Picture**: Path is stored in settings and updated live in the UI.

---

## Extensibility & Customization
- **Roles**: New roles can be added by creating a new directory under `profiles/` with the required files.
- **Tools**: Each role's `tools.yaml` can define new tools, dependencies, and scripts.
- **UI**: The modular widget/tab system allows for new sections to be added easily.

---

## Notable Features & Design Patterns
- **Centralized Config**: All paths and constants are defined in `config.py` for maintainability.
- **Separation of Concerns**: UI, core logic, and utilities are cleanly separated.
- **Batch Operations**: Environment setup supports batch install/uninstall with dependency management.
- **Fallback Logic**: Uses `paru` if `pacman` fails, increasing robustness for package management.
- **Custom Fonts & Theming**: Uses bundled fonts and supports dark/light themes.
- **Error Handling**: User-facing error messages in the UI, with critical errors highlighted.
- **Backup/Restore**: Settings are protected with automatic backup and restore features.

---

## File/Module Summaries
- **main.py**: App entry point, launches the main window.
- **config.py**: Central config for all paths, constants, and environment variables.
- **app/ui/windows/main_window.py**: Defines the main custom-shaped window, navigation, and content switching.
- **app/ui/widgets/side_buttons_panel.py**: Navigation panel with custom-shaped buttons.
- **app/ui/widgets/profile_pic.py**: Circular profile picture widget, loads/saves path from settings.
- **app/core/role.py**: Role management, content loading, and UI logic.
- **app/core/role_env_setup.py**: Handles environment setup, tool install/uninstall, dependency management, and tooltips.
- **app/core/settings.py**: Settings window, YAML management, backup/restore, and validation.
- **app/utils/roles_utils.py**: Role selection, YAML helpers, and directory management.
- **app/ui/tabs/wiki.py**: Wiki/knowledge base tab, searchable tips, and HTML content display.
- **app/roles/profiles/**: Role-specific content and configuration (materials, roadmap, tools, images).

---

## Conclusion
Exodia Assistant is a robust, extensible, and user-friendly application for Exodia OS, with a strong focus on modularity, customization, and maintainability. Its architecture supports easy addition of new roles, tools, and UI sections, making it a powerful platform for both users and developers. 