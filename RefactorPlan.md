# 🏗️ Exodia Assistant: Architectural Review & Refactor Plan

## 1. Architectural Review

### 1.1. Current Structure

- **Entry Point:** `main.py` launches a PyQt5 app, instantiating `CustomShapeWindow`.
- **App Logic:** Located in `app/core/` (`role.py`, `settings.py`), with large, multi-responsibility classes.
- **UI:** Split into `windows/`, `widgets/`, `tabs/`, and `keybinding/` under `app/ui/`.
- **Roles:** `app/roles/profiles/` contains per-role HTML, YAML, and images.
- **Assets:** All static files (HTML, images, icons, fonts) are under `assets/`.
- **Utils:** `app/utils/` contains helpers for fonts, HTML, roles, files, X11, and UI.
- **Config:** `config.py` is present but unused.
- **No tests** or clear separation between business logic and UI.

### 1.2. Architectural Issues

- **Tight Coupling:** UI and business logic are mixed (e.g., `Role` widget handles both UI and data).
- **Large Classes:** Monolithic files (`role.py`, `settings.py`, `roles_utils.py`) with hundreds of lines and multiple responsibilities.
- **Redundancy:** Similar logic for loading assets, roles, and HTML is repeated.
- **Unclear Boundaries:** No clear distinction between services, models, and UI.
- **Hardcoded Paths:** Asset and config paths are scattered and sometimes duplicated.
- **Difficult Testing:** No test structure; logic is not easily mockable or injectable.
- **UI Components:** Widgets are not fully reusable or isolated.
- **Configuration:** No centralized config or environment management.

---

## 2. Module Responsibilities

| Module/File                | Responsibility                                                                 |
|----------------------------|-------------------------------------------------------------------------------|
| `main.py`                  | App entry, launches main window                                               |
| `app/core/role.py`         | Role UI, role loading, business logic, asset loading (all mixed)              |
| `app/core/settings.py`     | Settings window UI, config file handling, theme/font logic                    |
| `app/ui/windows/`          | Main and internal window composition                                          |
| `app/ui/widgets/`          | Side panel, profile pic, button widgets                                       |
| `app/ui/tabs/`             | News, tweaks, wiki tab logic                                                  |
| `app/ui/keybinding/`       | Keybinding UI logic                                                           |
| `app/utils/roles_utils.py` | Role discovery, YAML read/write, role selection window                        |
| `app/utils/html_utils.py`  | HTML loading, asset path fixing                                               |
| `assets/`                  | Static files (HTML, images, icons, fonts)                                     |
| `app/roles/profiles/`      | Per-role HTML, YAML, images                                                   |
| `config.py`                | (Unused) Intended for global config                                           |

---

## 3. Proposed Directory Structure

```plaintext
exodia-assistant/
├── main.py
├── config.py
├── requirements.txt
├── README.md
├── assets/
│   ├── fonts/
│   ├── html/
│   ├── icons/
│   └── imgs/
├── app/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── role_manager.py      # Handles role CRUD, loading, saving
│   │   ├── settings_service.py  # Handles settings logic, config IO
│   │   ├── news_service.py      # Handles news fetching/parsing
│   │   └── config_loader.py     # Handles YAML/JSON config
│   ├── models/
│   │   ├── __init__.py
│   │   ├── role.py              # Role data model
│   │   └── settings.py          # Settings data model
│   ├── ui/
│   │   ├── windows/
│   │   │   ├── main_window.py
│   │   │   ├── internal_window.py
│   │   │   └── tweaks_window.py
│   │   ├── widgets/
│   │   │   ├── side_panel.py
│   │   │   ├── profile_pic.py
│   │   │   ├── custom_buttons.py
│   │   │   └── logo_widget.py
│   │   ├── tabs/
│   │   │   ├── roadmap_tab.py
│   │   │   ├── materials_tab.py
│   │   │   └── environment_tab.py
│   │   └── keybinding/
│   │       └── keybinding_widget.py
│   ├── roles/
│   │   ├── profiles/
│   │   │   ├── DevOps/
│   │   │   ├── Backend/
│   │   │   ├── Frontend/
│   │   │   └── MLOps/
│   │   ├── role.yaml
│   │   └── roles_utils.py
│   └── utils/
│       ├── font_utils.py
│       ├── html_utils.py
│       ├── file_utils.py
│       ├── x11_utils.py
│       └── ui_utils.py
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/
└── docs/
```

---

## 4. Refactor Roadmap

### **Phase 1: Infrastructure & Preparation**
- [ ] Set up `tests/` and `docs/` folders.
- [ ] Move all static assets to `assets/`.
- [ ] Create `models/` for data classes (Role, Settings).
- [ ] Create `core/` for business logic/services.
- [ ] Create `ui/` for all UI code, split by windows, widgets, tabs.

### **Phase 2: Decoupling & Modularization**
- [ ] Refactor `role.py`:
  - Move data logic to `role_manager.py` and `models/role.py`.
  - Move UI logic to `ui/widgets/role_widget.py`.
- [ ] Refactor `settings.py`:
  - Move config IO to `settings_service.py`.
  - Move UI to `ui/windows/settings_window.py`.
- [ ] Extract all business logic from UI classes into services.
- [ ] Centralize config and path management in `config.py` and `core/config_loader.py`.
- [ ] Refactor `roles_utils.py` into pure logic (no UI).
- [ ] Move all role selection UI to a dedicated widget.

### **Phase 3: UI Componentization**
- [ ] Isolate reusable widgets (side panel, buttons, profile pic, etc.).
- [ ] Move tab logic into separate files (one per tab).
- [ ] Use signals/slots or callbacks for UI-service communication.
- [ ] Standardize UI styling and theming.

### **Phase 4: Testing & Documentation**
- [ ] Add unit tests for all services and models.
- [ ] Add integration tests for UI flows.
- [ ] Document all modules and public APIs.
- [ ] Add docstrings and type hints throughout.

### **Phase 5: Configuration & Extensibility**
- [ ] Use a single config loader for YAML/JSON.
- [ ] Allow for environment-based config overrides.
- [ ] Document how to add new roles, tabs, or widgets.

---

## 5. Naming, Modularity, and Configuration

- **Naming:** Use descriptive, consistent names (e.g., `role_manager.py`, `settings_service.py`, `side_panel.py`).
- **Modularity:** Each module should have a single responsibility. UI, business logic, and data models must be separated.
- **Configuration:** All paths, constants, and environment settings should be in `config.py` or a config loader.
- **Testing:** All business logic should be testable without UI.

---

## 6. Shared Logic & Reusable Components

- **Services:** Extract logic for roles, settings, news, etc., into service classes.
- **Models:** Use data classes for roles, settings, etc.
- **UI Components:** Isolate widgets (side panel, buttons, etc.) for reuse.
- **Utils:** Only pure, stateless helpers should remain in `utils/`.

---

## 7. Example: Role Management Refactor

- `app/core/role_manager.py`: Handles loading, saving, and listing roles.
- `app/models/role.py`: Data class for a Role.
- `app/ui/widgets/role_widget.py`: UI for displaying a role.
- `app/roles/roles_utils.py`: Pure logic for role discovery, YAML IO.

---

## 8. Configuration & Testing Improvements

- **Centralize config** in `config.py` and `core/config_loader.py`.
- **Add tests** for all services and models.
- **Document** all modules and APIs.
- **Use dependency injection** for services in UI classes.

---

## 9. Migration Steps

1. **Prepare new folders** (`models/`, `core/`, `ui/`, `tests/`).
2. **Move and split logic** as per the roadmap.
3. **Refactor imports** and update all references.
4. **Test each phase** before proceeding.
5. **Document** as you go.

---

## 10. References

- See the `README.md` for further structure and clean code guidelines.
- Use the `structure.txt` as a reference for asset and profile organization.

---

**By following this plan, your app will be modular, maintainable, and ready for long-term growth.**

---

Let me know if you want a more detailed breakdown for any specific module or a sample refactored file!