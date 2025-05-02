# Exodia Assistant App - Developer Documentation

## Table of Contents
1. [Overview](#overview)
2. [Project Structure](#project-structure)
3. [Main Components](#main-components)
4. [Development Environment Setup](#development-environment-setup)
5. [Development Workflow](#development-workflow)
6. [Adding New Features](#adding-new-features)
7. [Styling Guidelines](#styling-guidelines)
8. [Contributing](#contributing)

## Overview

Exodia Assistant is a comprehensive helper application for Exodia OS. It provides users with easy access to system information, documentation, keybindings, news updates, and more in an elegant, custom-shaped interface.

The application is built using Python and PyQt5, featuring a custom-shaped window with a modern UI design. It follows a modular architecture where different components handle specific functionalities.

### Key Features

- **Welcome Screen**: Introduction to Exodia OS
- **News Updates**: Latest news and updates fetched from the Exodia OS repository
- **Keybinding Reference**: Searchable documentation for keyboard shortcuts
- **Wiki**: Searchable knowledge base for Exodia OS
- **Tweaks**: System configuration options
- **Roles**: User-selectable profiles for different use cases
- **Developers**: Information about the Exodia OS development team
- **Custom UI**: Elegant, modern interface with custom-shaped window

## Project Structure

The project follows this directory structure:

```
exodia-assistant-app/
├── README.md                 # Basic project information
├── DEVELOPMENT.md            # This developer documentation
├── TODO.md                   # Planned features and improvements
├── git-push.sh               # Script for pushing changes to Git
├── imgs/                     # Images used in documentation
├── preview.png               # Preview image for README
└── src/                      # Source code
    └── files/
        └── exodia-assistant/ # Main application code
            ├── Fonts/        # Custom fonts used in the app
            ├── HTML-files/   # HTML content for different sections
            │   ├── Keybinding/
            │   └── tips/
            ├── icons/        # App icons
            ├── imgs/         # Images used in the app
            │   ├── Keybinding/
            │   ├── Showcase/
            │   ├── team/
            │   └── tips/
            ├── roles/        # Role system files
            │   └── profiles/ # Role profiles
            ├── main_window.py            # Main window implementation
            ├── internal_window.py        # Internal window for content
            ├── side_buttons_panel.py     # Side panel with buttons
            ├── side_buttons_panel_content.py # Content for side panel buttons
            ├── utils.py                  # Utility functions
            ├── keybinding.py             # Keybinding functionality
            ├── wiki.py                   # Wiki functionality
            ├── news.py                   # News functionality
            ├── tweaks.py                 # Tweaks functionality
            └── settings.py               # Settings functionality
```

## Main Components

### Main Window (`main_window.py`)

The `CustomShapeWindow` class is the main window of the application. It:
- Creates a custom-shaped window using a polygon mask
- Sets up the window flags and attributes
- Initializes the UI components
- Handles window controls (minimize, close)
- Manages the display of different content types

### Internal Window (`internal_window.py`)

The `InternalWindow` class is responsible for displaying content within the main window. It provides a container for different types of content.

### Side Button Panel (`side_buttons_panel.py`)

The `CustomButtonPanel` class creates the side panel with buttons for navigating between different sections of the app.

### Button Content (`side_buttons_panel_content.py`)

The `ButtonContent` class manages the content displayed when different buttons are clicked. It handles:
- Welcome content
- News updates
- Keybinding reference
- Wiki content
- Tweaks options
- Role selection and display
- Developer information

### Roles System (`roles/role.py`, `roles/roles_utils.py`)

The roles system allows users to select different profiles or configurations:
- `Role` class manages the display of role content
- `RoleSelectionWindow` provides a UI for selecting roles
- Roles are stored in the `roles/profiles/` directory
- Role selection is saved to a YAML file

### Utility Functions (`utils.py`)

Contains utility functions used throughout the application:
- `loadPredatorFont()`: Loads the custom Predator font
- `loadHTMLContent()`: Loads HTML content from files
- `contentButtonMask()`: Creates custom button masks

## Development Environment Setup

### Prerequisites

- Python 3.6 or higher
- PyQt5
- PyYAML
- python-xlib

### Installation for Development

1. Clone the repository:
   ```bash
   git clone https://github.com/Exodia-OS/exodia-apps.git
   cd exodia-apps/exodia-assistant-app
   ```

2. Install dependencies:
   ```bash
   sudo pacman -S python-xlib exodia-pip-venv python-pyqt5
   cd src/files/exodia-assistant/
   pip install -r libs.txt
   ```

3. Run the application:
   ```bash
   python main.py
   ```

## Development Workflow

1. Create a new branch with your GitHub username:
   ```bash
   git checkout -b dev-yourusername
   ```

2. Make your changes to the codebase

3. Test your changes by running the application

4. Commit and push your changes:
   ```bash
   ./git-push.sh -m "your commit message"
   ```

5. Create a pull request on GitHub

## Adding New Features

### Adding a New Section

To add a new section to the application:

1. Create a new Python file for your section (e.g., `my_section.py`)
2. Implement the necessary functionality
3. Add a method to display your section in `side_buttons_panel_content.py`
4. Add a button for your section in `side_buttons_panel.py`
5. Connect the button to your display method in `main_window.py`

### Adding a New Role

To add a new role:

1. Create a new directory in `roles/profiles/` with the name of your role
2. Add an `index.html` file with the content for your role
3. Add any additional resources needed by your role

## Styling Guidelines

The application uses a consistent styling approach:

- **Colors**: Primary color is `#00B0C8` (cyan), background is `#151A21` (dark blue-gray)
- **Fonts**: Custom "Predator" font for headings, system fonts for body text
- **UI Elements**: Custom-shaped buttons and windows with polygon masks
- **Layout**: Clean, spacious layout with clear visual hierarchy

When adding new UI elements, maintain consistency with the existing design.

## Contributing

1. Fork the repository
2. Create a new branch with your GitHub username
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Code Style

- Follow PEP 8 guidelines for Python code
- Use meaningful variable and function names
- Add comments for complex logic
- Document public functions and classes

### Documentation

When adding new features, update the relevant documentation:
- Add comments in the code
- Update this DEVELOPMENT.md file if necessary
- Update the README.md if user-facing features change

### Testing

Before submitting a pull request:
- Test your changes on different screen sizes
- Ensure all features work as expected
- Check for any visual glitches or inconsistencies