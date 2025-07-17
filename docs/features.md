# Adding New Features & Roles

This guide explains how to extend the Exodia Assistant App with new sections or user roles.

## Adding a New Section
1. **Create a new Python file** for your section (e.g., `my_section.py`) in the appropriate directory (usually `ui/tabs/` or `ui/widgets/`).
2. **Implement your section's logic and UI.**
3. **Add a display method** for your section in `side_buttons_panel_content.py`.
4. **Add a button** for your section in `side_buttons_panel.py`.
5. **Connect the button** to your display method in `main_window.py`.

**Example:**
```python
# In side_buttons_panel_content.py
def show_my_section(self):
    # Load and display your section's content
    pass
```

## Adding a New Role
1. **Create a new directory** in `roles/profiles/` with your role's name.
2. **Add an `index.html`** file with the content for your role.
3. **Add any additional resources** (images, TOML, etc.) needed by your role.
   - Tool configuration is now stored in a `tools.toml` file (not YAML).
   - The "Explore Role" tab now allows you to browse all official and community roles, install or uninstall them live (without leaving the tab), search/filter roles, and see which are installed. The UI updates instantly after each action, and the background color for the roles area is now `#0E1218` for improved clarity.

**Example Directory:**
```
roles/profiles/MyRole/
    index.html
    roadmap.png
    tools.toml
```

## Extending Existing Features
- To add new tweaks, keybindings, or wiki entries, update the relevant HTML or TOML files in `assets/html/` or `roles/profiles/`.
- For new UI widgets, add them to `ui/widgets/` and integrate as needed.
- The Environment Setup tab now displays the total number of tools and installed tools in the UI.

See `components.md` for where to place new code. 