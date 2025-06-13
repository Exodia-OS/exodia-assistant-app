# Exodia Assistant Application Structure

## Overview
The Exodia Assistant application is organized into several key directories and files, each serving a specific purpose in the application's functionality. This document provides a detailed explanation of the structure and purpose of each component.

## Directory Structure

### 1. Fonts Directory
```
Fonts/
├── Squares-Black-Italic.otf
├── Squares-Black.otf
├── Squares-Bold-Italic.otf
├── Squares-Bold.otf
├── Squares-Italic.otf
├── Squares-Light-italic.otf
├── Squares-Light.otf
├── Squares-Regular.otf
├── Squares-Thin-Italic.otf
└── Squares-Thin.otf
```
- Contains the custom "Squares" font family used throughout the application
- Includes various weights (Thin, Light, Regular, Bold, Black) and styles (Regular, Italic)
- Used for consistent typography across the application

### 2. HTML-files Directory
```
HTML-files/
├── displayDevelopersContent.html
├── displayRoleContent.html
├── displayTweaksContent.html
├── displayWelcomeContent.html
├── ExploreRole.html
├── HowtoCreateYourOwnRole.html
├── Keybinding/
│   ├── BSPWM.html
│   ├── DWM.html
│   └── I3WM.html
├── News.html
└── tips/
    ├── Adding-Music.html
    ├── bspwm-themes.html
    └── ...
```
- Contains all HTML content displayed in the application
- Organized by feature (Keybinding, tips, etc.)
- Includes documentation and help content
- Window manager-specific keybinding documentation

### 3. Icons Directory
```
icons/
├── exodia-blue.png
├── exodia-cyan.png
├── exodia-green.png
├── exodia-magenta.png
├── exodia.png
├── exodia-red.png
├── exodia-violet.png
├── exodia-yellow.png
├── logos.gif
└── Predator.png
```
- Application icons and logos
- Different color variants of the Exodia logo
- Predator logo for branding

### 4. Images Directory
```
imgs/
├── desktop.png
├── FreePalestine.png
├── Keybinding/
├── Showcase/
├── team/
└── tips/
```
- Contains all application images
- Organized by category (Keybinding, Showcase, team, tips)
- Includes screenshots, team photos, and tutorial images

### 5. Core Python Files

#### Main Application Files
- `main.py`: Application entry point
- `main_window.py`: Main window implementation
- `internal_window.py`: Internal window management
- `utils.py`: Utility functions

#### Feature Modules
- `keybinding.py`: Keybinding management
- `news.py`: News feed functionality
- `profile_pic.py`: Profile picture handling
- `settings.py`: Application settings
- `tweaks.py`: System tweaks
- `wiki.py`: Wiki functionality

#### UI Components
- `side_buttons_panel.py`: Side panel implementation
- `side_buttons_panel_content.py`: Side panel content management

### 6. Roles Directory
```
roles/
├── profiles/
│   ├── Backend/
│   ├── DevOps/
│   ├── Frontend/
│   └── MLOps/
├── role.py
├── roles_utils.py
└── role.yaml
```
- Contains role-specific configurations and content
- Each role has its own directory with:
  - `materials.html`: Learning materials
  - `roadmap.html`: Career roadmap
  - `tools.yaml`: Tool configurations
  - `roadmap.png`: Roadmap visualization

### 7. Configuration Files
- `libs.txt`: Python dependencies
- `role.yaml`: Role configuration
- Various YAML files for tool configurations

## Key Components

### 1. Role Management
- `roles/role.py`: Role management implementation
- `roles/roles_utils.py`: Role utility functions
- `roles/role.yaml`: Role configuration

### 2. UI Components
- `main_window.py`: Main application window
- `internal_window.py`: Content window management
- `side_buttons_panel.py`: Navigation panel

### 3. Content Management
- HTML files for different sections
- Image assets for visual content
- Role-specific content in profiles

### 4. Configuration
- YAML files for tool configurations
- Role-specific settings
- Application settings

## File Purposes

### Core Files
1. `main.py`
   - Application entry point
   - Initializes the main window
   - Sets up the application environment

2. `main_window.py`
   - Implements the main application window
   - Manages window properties and layout
   - Handles window events

3. `internal_window.py`
   - Manages internal content windows
   - Handles content display
   - Manages window transitions

### Feature Modules
1. `keybinding.py`
   - Manages keyboard shortcuts
   - Displays keybinding documentation
   - Handles keybinding updates

2. `news.py`
   - Fetches and displays news
   - Manages news updates
   - Handles news formatting

3. `settings.py`
   - Manages application settings
   - Handles user preferences
   - Saves configuration changes

### Utility Files
1. `utils.py`
   - Common utility functions
   - Helper methods
   - Shared functionality

2. `roles_utils.py`
   - Role management utilities
   - Role configuration handling
   - Role data processing

## Configuration Structure

### Role Configuration
```yaml
# role.yaml
role: "DevOps"  # Current selected role
```

### Tool Configuration
```yaml
# tools.yaml
category:
  - name: "Tool Name"
    pkg: "package-name"
    status: "Installed"
    pre-install: "command1, command2"
    post-install: "command1, command2"
```

## Dependencies
- Python 3.x
- PyQt5
- PyYAML
- Required Python packages listed in `libs.txt` 

the full structure

```bash
exodia-assistant

├── Fonts

│   ├── Squares-Black-Italic.otf

│   ├── Squares-Black.otf

│   ├── Squares-Bold-Italic.otf

│   ├── Squares-Bold.otf

│   ├── Squares-Italic.otf

│   ├── Squares-Light-italic.otf

│   ├── Squares-Light.otf

│   ├── Squares-Regular.otf

│   ├── Squares-Thin-Italic.otf

│   └── Squares-Thin.otf

├── HTML-files

│   ├── displayDevelopersContent.html

│   ├── displayRoleContent.html

│   ├── displayTweaksContent.html

│   ├── displayWelcomeContent.html

│   ├── ExploreRole.html

│   ├── HowtoCreateYourOwnRole.html

│   ├── Keybinding

│   │   ├── BSPWM.html

│   │   ├── DWM.html

│   │   └── I3WM.html

│   ├── News.html

│   └── tips

│       ├── Adding-Music.html

│       ├── bspwm-themes.html

│       ├── Change-Fonts.html

│       ├── change-theme-and-icons.html

│       ├── Changing-SDDM-User-Picture.html

│       ├── Create-Your-Own-Theme.html

│       ├── Fix-Cava-Module.html

│       ├── pacman-tips.html

│       ├── PGP-signature-Error.html

│       ├── Set-Keyboard-Layout.html

│       ├── Setup-Custom-Monitors-Config.html

│       ├── Setup-Polybar-Modules.html

│       └── unable-to-lock-database.html

├── icons

│   ├── exodia-blue.png

│   ├── exodia-cyan.png

│   ├── exodia-green.png

│   ├── exodia-magenta.png

│   ├── exodia.png

│   ├── exodia-red.png

│   ├── exodia-violet.png

│   ├── exodia-yellow.png

│   ├── logos.gif

│   └── Predator.png

├── imgs

│   ├── desktop.png

│   ├── FreePalestine.png

│   ├── Keybinding

│   │   ├── bspwm.png

│   │   ├── dwm.png

│   │   ├── i3wm.png

│   │   └── Note.png

│   ├── Showcase

│   │   ├── 10.png

│   │   ├── 1.png

│   │   ├── 2.png

│   │   ├── 3.png

│   │   ├── 4.png

│   │   ├── 5.png

│   │   ├── 6.png

│   │   ├── 7.png

│   │   ├── 8.png

│   │   ├── 9.png

│   │   ├── bspwm.gif

│   │   ├── dwm.gif

│   │   └── I3WM.gif

│   ├── team

│   │   ├── Austin.png

│   │   ├── Budas.png

│   │   ├── DonSom3a.png

│   │   ├── Joe.png

│   │   ├── NahianAdnan.png

│   │   └── Ozil.png

│   └── tips

│       ├── AddingMusic

│       │   └── preview.png

│       ├── BSPWMThemes

│       │   ├── 10.png

│       │   ├── 11.png

│       │   ├── 12.png

│       │   ├── 13.png

│       │   ├── 14.png

│       │   ├── 15.png

│       │   ├── 1.png

│       │   ├── 2.png

│       │   ├── 3.png

│       │   ├── 4.png

│       │   ├── 5.png

│       │   ├── 6.png

│       │   ├── 7.png

│       │   ├── 8.png

│       │   └── 9.png

│       ├── cava

│       │   ├── 1.png

│       │   └── 2.png

│       ├── ChangeFonts

│       │   ├── 1.png

│       │   ├── 2.png

│       │   ├── 3.png

│       │   ├── 4.png

│       │   ├── 5.png

│       │   └── 6.png

│       ├── ChangeThemeAndIcons

│       │   └── 1.png

│       ├── CreateCustomTheme

│       │   ├── 1.png

│       │   ├── 2.png

│       │   ├── AddColorScheme.png

│       │   ├── GeneratedColorScheme.png

│       │   ├── Hint.png

│       │   ├── polybar-1.png

│       │   ├── polybar-2.png

│       │   ├── polybar-2.png~

│       │   ├── polybar-3.png

│       │   ├── preview.png

│       │   └── warning.png

│       ├── github

│       │   ├── 1.png

│       │   ├── 2.png

│       │   ├── 3.png

│       │   ├── 4.png

│       │   ├── 5.png

│       │   ├── 6.png

│       │   └── github.png

│       ├── keyboardLayouts

│       │   ├── 0.png

│       │   ├── ar.png

│       │   └── en.png

│       ├── monitors

│       │   ├── 1.png

│       │   ├── 2.png

│       │   ├── 3.png

│       │   ├── 4.png

│       │   └── Note.png

│       ├── multiBars

│       │   ├── 0.png

│       │   ├── 1.png

│       │   ├── 2.png

│       │   ├── 3.png

│       │   ├── 4.png

│       │   ├── 5.png

│       │   ├── 6.png

│       │   └── 7.png

│       ├── sddm

│       │   ├── 0.png

│       │   ├── 1.png

│       │   ├── 2.png

│       │   ├── 3.png

│       │   └── 4.png

│       └── weather

│           ├── 0.png

│           ├── 1.png

│           ├── 2.png

│           ├── 3.png

│           ├── 4.png

│           ├── 5.png

│           └── 6.png

├── internal_window.py

├── keybinding.py

├── libs.txt

├── main.py

├── main_window.py

├── news.py

├── profile_pic.py

├── __pycache__

│   ├── internal_window.cpython-313.pyc

│   ├── keybinding.cpython-313.pyc

│   ├── main_window.cpython-313.pyc

│   ├── news.cpython-313.pyc

│   ├── profile_pic.cpython-313.pyc

│   ├── settings.cpython-313.pyc

│   ├── side_buttons_panel_content.cpython-313.pyc

│   ├── side_buttons_panel.cpython-313.pyc

│   ├── tweaks.cpython-313.pyc

│   ├── utils.cpython-313.pyc

│   └── wiki.cpython-313.pyc

├── roles

│   ├── __init__.py

│   ├── profiles

│   │   ├── Backend

│   │   │   ├── materials.html

│   │   │   ├── roadmap.html

│   │   │   ├── roadmap.png

│   │   │   └── tools.yaml

│   │   ├── DevOps

│   │   │   ├── DevOpsBurger.jpg

│   │   │   ├── docker.sh

│   │   │   ├── materials.html

│   │   │   ├── roadmap.html

│   │   │   ├── roadmap.png

│   │   │   ├── tools.png

│   │   │   └── tools.yaml

│   │   ├── Frontend

│   │   │   ├── materials.html

│   │   │   ├── roadmap.html

│   │   │   ├── roadmap.png

│   │   │   └── tools.yaml

│   │   └── MLOps

│   │       ├── materials.html

│   │       ├── roadmap.html

│   │       ├── roadmap.png

│   │       └── tools.yaml

│   ├── __pycache__

│   │   ├── __init__.cpython-313.pyc

│   │   ├── role.cpython-313.pyc

│   │   └── roles_utils.cpython-313.pyc

│   ├── role.py

│   ├── roles_utils.py

│   └── role.yaml

├── settings.py

├── side_buttons_panel_content.py

├── side_buttons_panel.py

├── tweaks.py

├── utils.py

└── wiki.py

31 directories, 189 files
```