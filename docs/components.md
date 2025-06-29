# Main Components

This document explains the core components of the Exodia Assistant App, their responsibilities, and how they interact.

## Main Window (`main_window.py`)
- **Class:** `CustomShapeWindow`
- **Location:** `src/files/exodia-assistant/app/ui/windows/main_window.py`
- **Responsibilities:**
  - Creates the main application window with a custom polygon shape
  - Sets window flags and attributes
  - Initializes UI components (side panel, content area)
  - Handles window controls (minimize, close)
  - Manages switching between content sections

## Internal Window (`internal_window.py`)
- **Class:** `InternalWindow`
- **Location:** `src/files/exodia-assistant/app/ui/windows/internal_window.py`
- **Responsibilities:**
  - Container for displaying different content types
  - Used by the main window to show section content

## Side Button Panel (`side_buttons_panel.py`)
- **Class:** `CustomButtonPanel`
- **Location:** `src/files/exodia-assistant/app/ui/widgets/side_buttons_panel.py`
- **Responsibilities:**
  - Renders the vertical navigation panel
  - Contains buttons for each app section
  - Handles button click events

## Button Content (`side_buttons_panel_content.py`)
- **Class:** `ButtonContent`
- **Location:** `src/files/exodia-assistant/app/ui/widgets/side_buttons_panel_content.py`
- **Responsibilities:**
  - Displays content for each section (Welcome, News, Keybindings, Wiki, Tweaks, Roles, Developers)
  - Loads HTML or dynamic content as needed

## Roles System
- **Files:**
  - `roles/role.py`: Role display logic
  - `roles/roles_utils.py`: Role utilities
  - `roles/profiles/`: Role profile data (HTML, TOML, images)
  - `core/role_env_setup.py`: Environment Setup tab logic
- **Responsibilities:**
  - Allow users to select and view different roles/profiles
  - Store and load role data from TOML/HTML
  - Environment Setup tab displays all tools, grouped by category, and shows the total number of tools and installed tools in the UI (between the search bar and Update Status button)

## Utility Functions (`utils/`)
- **Files:**
  - `file_utils.py`, `font_utils.py`, `html_utils.py`, `roles_utils.py`, `ui_utils.py`, `x11_utils.py`
- **Responsibilities:**
  - Provide reusable helpers for file I/O, font loading, HTML rendering, role management, UI, and X11 integration

## Other UI Components
- **Tabs:** News, Tweaks, Wiki (in `ui/tabs/`)
- **Widgets:** Profile picture, side panels (in `ui/widgets/`)
- **Keybinding:** Keybinding reference (in `ui/keybinding/`)

See the source files for class/method details and usage examples. 