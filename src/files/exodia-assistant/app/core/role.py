#####################################
#                                   #
#  @author      : 00xWolf           #
#    GitHub    : @mmsaeed509       #
#    Developer : Mahmoud Mohamed   #
#  﫥  Copyright : Exodia OS         #
#                                   #
#####################################

import os, sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QPushButton, QLabel, QHBoxLayout, QTabWidget, QFrame, QTextBrowser, QCheckBox, QGroupBox, QLineEdit, QGridLayout, QMessageBox, QApplication, QDialog
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDesktopServices
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ..utils import font_utils, html_utils, roles_utils
from .role_env_setup import create_setup_environment_tab
from config import USER_CONFIG_DIR, ROLES_PROFILES_DIR

def open_url(url):
    """
    Open a URL in the default web browser.

    Args:
        url (QUrl or str): The URL to open
    """
    if isinstance(url, str):
        url = QUrl(url)
    print(f"Opening URL: {url.toString()}")
    QDesktopServices.openUrl(url)


class Role(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Set the geometry (position and size) of the widget
        self.setGeometry(0, 0, 800, 600)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)  # Make the background transparent

        # Use predator font from font_utils.py
        self.predator_font = None
        self.predator_font = font_utils.loadPredatorFont()
        if self.predator_font:
            # Adjust the font size to 12 as it was before
            self.predator_font.setPointSize(12)

        # Initialize layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Create a scroll area for the content
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("background-color: transparent; border: none;")

        # Create a widget to hold the content
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)

        # Set the content widget in the scroll area
        self.scroll_area.setWidget(self.content_widget)

        # Add the scroll area to the main layout
        self.layout.addWidget(self.scroll_area)

        # Available roles
        self.roles = ["Select a Role", "Manage Your Role", "Create a Role", "Explore Role"]

        # Role selection window
        self.role_selection_window = None

        # Internal window reference for content display
        self.internal_window = None

    def load_role_content(self, role_name=None, internal_window=None, back_callback=None):
        """
        Load the content for a specific role.

        Args:
            role_name (str): The name of the role to load
            internal_window (QWidget): The window to display the content in
            back_callback (function): Callback function to execute when the Back button is clicked

        Returns:
            str: HTML content to display, or empty string if content is handled by display_create_role or display_manage_role
        """
        # Store the internal window reference if provided
        if internal_window:
            self.internal_window = internal_window

        # Path to the profiles directory
        # config_dir = os.path.expanduser("~/.config/exodia-assistant")
        # os.makedirs(config_dir, exist_ok=True)  # Ensure directory exists
        # roles_dir = os.path.join(config_dir, "/profiles")
        roles_dir = ROLES_PROFILES_DIR
        os.makedirs(roles_dir, exist_ok=True)  # Ensure directory exists
        available_roles = [d for d in os.listdir(roles_dir) if os.path.isdir(os.path.join(roles_dir, d))]
        if not available_roles:
            # Try to install the default role 'CS Student' from the official repo
            from PyQt5.QtWidgets import QMessageBox
            ok, msg = roles_utils.update_role_from_system('CS Student', 'official')
            if ok:
                # After installing, prompt the user to select a role
                self.show_role_selection_window()
            else:
                QMessageBox.critical(self, "Default Role Install Failed", f"Failed to install the default role 'CS Student':\n{msg}")
            # Re-check available roles after install attempt
            available_roles = [d for d in os.listdir(roles_dir) if os.path.isdir(os.path.join(roles_dir, d))]
            if not available_roles:
                return "<div style='color: #B00020; font-size: 18px;'>No roles are installed and the default role could not be installed. Please check your roles repo.</div>"

        text = """<div style="font-family: {}; color: #00B0C8; line-height: 1.6; font-size: 18px; max-width: 800px; margin: auto; padding: 0 20px;">                    
                    <h4 style="color: #00C8B0; font-size: 20px; margin-bottom: 15px;"> Role Overview </h4>
                </div>""".format(self.predator_font.family())

        # If no role is specified, load the index page
        if role_name is None or role_name not in self.roles:
            # return text
            return html_utils.loadHTMLContent('../../assets/html', 'role.html', self.predator_font.family())

        # If the role is "Select a Role", show the role selection window
        elif role_name == "Select a Role":
            self.show_role_selection_window()
            return html_utils.loadHTMLContent('../../assets/html', 'role.html', self.predator_font.family())

        # If the role is "Create a Role", use the display_create_role method if internal_window is available
        elif role_name == "Create a Role":
            if self.internal_window:
                self.display_create_role(back_callback)
                return ""  # Return empty string as content will be handled by display_create_role
            else:
                # Fallback to the old method if internal_window is not available
                return html_utils.loadHTMLContent('../../assets/html', 'HowtoCreateYourOwnRole.html', self.predator_font.family())

        # If the role is "Explore Role", use the display_create_role method if internal_window is available
        elif role_name == "Explore Role":
            if self.internal_window:
                self.display_explore_role(back_callback)
                return ""  # Return empty string as content will be handled by display_create_role
            else:
                # Fallback to the old method if internal_window is not available
                return f"""<div style="font-family: {self.predator_font.family()}; color: #00B0C8; line-height: 1.6; font-size: 18px; max-width: 800px; margin: auto; padding: 0 20px;">
                    <h4 style="color: #00C8B0; font-size: 20px; margin-bottom: 15px;">{role_name}</h4>
                    <p>This category is under development. will be available soon!</p>
                </div>"""

        # If the role is "Manage Your Role", use the display_manage_role method if internal_window is available
        elif role_name == "Manage Your Role":
            if self.internal_window:
                self.display_manage_role(back_callback)
                return ""  # Return empty string as content will be handled by display_manage_role
            else:
                # Fallback to the old method if internal_window is not available
                return f"""<div style="font-family: {self.predator_font.family()}; color: #00B0C8; line-height: 1.6; font-size: 18px; max-width: 800px; margin: auto; padding: 0 20px;">
                    <h4 style="color: #00C8B0; font-size: 20px; margin-bottom: 15px;">{role_name}</h4>
                    <p>This category is under development. More features will be available soon!</p>
                </div>"""

        else:
            # Check if the role is a directory in the profiles directory
            available_roles = roles_utils.get_available_roles()
            if role_name in available_roles:
                # Load content from the role directory
                role_dir = os.path.join(roles_dir, role_name)
                index_file = os.path.join(role_dir, "index.html")

                # Check if the index file exists
                if os.path.exists(index_file):
                    try:
                        with open(index_file, 'r') as file:
                            content = file.read()
                        return f"<div style='font-family: {self.predator_font.family()};'>{content}</div>"
                    except Exception as e:
                        return f"<div style='color: #00B0C8; font-family: {self.predator_font.family()};'>Error loading role content: {str(e)}</div>"
                else:
                    # If no index file, create a default content
                    return f"""<div style="font-family: {self.predator_font.family()}; color: #00B0C8; line-height: 1.6; font-size: 18px; max-width: 800px; margin: auto; padding: 0 20px;">
                        <h4 style="color: #00C8B0; font-size: 20px; margin-bottom: 15px;">{role_name} Role</h4>
                        <p>This role is available but does not have an index.html file.</p>
                    </div>"""
            else:
                # Legacy support for old role files
                file_path = os.path.join(roles_dir, f"{role_name}.html")

                # Check if the file exists
                if not os.path.exists(file_path):
                    return f"<div style='color: #00B0C8; font-family: {self.predator_font.family()};'>Role content not found: {file_path}</div>"

                # Read the file content and apply the Predator Font
                try:
                    with open(file_path, 'r') as file:
                        content = file.read()
                    return f"<div style='font-family: {self.predator_font.family()};'>{content}</div>"
                except Exception as e:
                    return f"<div style='color: #00B0C8; font-family: {self.predator_font.family()};'>Error loading role content: {str(e)}</div>"

    def get_available_roles(self):
        return self.roles

    def display_create_role(self, back_callback=None):
        """
        Display the "Create a Role" content with a Back button and scroll area
        similar to the ones in tweaks.py.

        Args:
            back_callback (function): Callback function to execute when the Back button is clicked
        """
        # Clear the existing layout
        if not self.internal_window.layout():
            self.internal_window.setLayout(QVBoxLayout())

        # Clear previous content
        while self.internal_window.layout().count():
            item = self.internal_window.layout().takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # Create a "Back" button to return to the roles view
        back_button = QPushButton("Back")
        back_button.setFont(self.predator_font)
        back_button.setFixedSize(100, 40)
        back_button.setStyleSheet(
            """
            QPushButton {
                background-color: #006C7A;
                color: white;
                border: none;
                font-size: 18px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #004F59;
            }
            QPushButton:pressed {
                background-color: #005F78;
            }
            """
        )

        # Connect the Back button to the callback function or a default function
        if back_callback:
            back_button.clicked.connect(back_callback)
        else:
            # Default behavior if no callback is provided
            back_button.clicked.connect(lambda: self.internal_window.setLayout(QVBoxLayout()))

        # Add the "Back" button to the top layout
        top_layout = QHBoxLayout()
        top_layout.addWidget(back_button, alignment=Qt.AlignLeft)

        top_widget = QWidget()
        top_widget.setLayout(top_layout)
        self.internal_window.layout().addWidget(top_widget)

        # Create the content for the "Create a Role" section
        html_content = html_utils.loadHTMLContent('../../assets/html', 'HowtoCreateYourOwnRole.html', self.predator_font.family())


        # Create a label for the content
        content_label = QLabel()
        content_label.setTextFormat(Qt.RichText)
        content_label.setWordWrap(True)
        content_label.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        content_label.setText(html_content)

        # Create a scroll area for the content
        scroll_area = QScrollArea()
        scroll_area.setGeometry(40, 20, 1100, 600)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setWidgetResizable(True)

        # Create a widget to hold the content
        scroll_content = QWidget()
        scroll_content.setStyleSheet("background-color: #151A21;")
        scroll_area.setWidget(scroll_content)

        # Add the content label to the scroll content
        layout = QVBoxLayout(scroll_content)
        layout.addWidget(content_label)

        # Style the scroll area
        scroll_area.setStyleSheet("""
            QScrollArea { 
                border: none;
                padding: 0;
                background-color: #151A21;
            }
            QScrollBar:vertical {
                background: #151A21;
                width: 10px;
                margin: 0 0 0 0;
            }
            QScrollBar::handle:vertical {
                background: #00B0C8;
                border-radius: 0px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background: #00B0C8;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: #151A21;
            }
        """)

        # Style the content label
        content_label.setFont(self.predator_font)
        content_label.setStyleSheet(
            f"color: #00B0C8; font-size: 18px; background-color: #151A21; padding: 10px;"
            f"font-family: '{self.predator_font.family()}';"
        )
        content_label.setTextInteractionFlags(Qt.TextSelectableByMouse)

        # Add the scroll area to the internal window
        self.internal_window.layout().addWidget(scroll_area)

    def display_explore_role(self, back_callback=None):
        """
        Display the "Explore Role" content with a Back button, search bar, and a grid of roles (official/community),
        showing install/uninstall options and installed status.
        """
        from ..utils import roles_utils
        import subprocess
        import time
        # Clear the existing layout
        if not self.internal_window.layout():
            self.internal_window.setLayout(QVBoxLayout())
        while self.internal_window.layout().count():
            item = self.internal_window.layout().takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # Back button
        back_button = QPushButton("Back")
        back_button.setFont(self.predator_font)
        back_button.setFixedSize(100, 40)
        back_button.setStyleSheet("""
            QPushButton {
                background-color: #006C7A;
                color: white;
                border: none;
                font-size: 18px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #004F59;
            }
            QPushButton:pressed {
                background-color: #005F78;
            }
        """)
        if back_callback:
            back_button.clicked.connect(back_callback)
        else:
            back_button.clicked.connect(lambda: self.internal_window.setLayout(QVBoxLayout()))
        top_layout = QHBoxLayout()
        top_layout.addWidget(back_button, alignment=Qt.AlignLeft)

        # Title
        title_label = QLabel("Explore Roles (Official & Community)")
        title_label.setFont(self.predator_font)
        title_label.setStyleSheet(f"color: #00B0C8; font-size: 24px; font-weight: bold; font-family: '{self.predator_font.family()}';")
        title_label.setAlignment(Qt.AlignCenter)
        top_layout.addWidget(title_label, alignment=Qt.AlignCenter)
        spacer = QWidget()
        spacer.setFixedSize(100, 40)
        top_layout.addWidget(spacer, alignment=Qt.AlignRight)
        top_widget = QWidget()
        top_widget.setLayout(top_layout)
        self.internal_window.layout().addWidget(top_widget)

        # Search bar
        search_layout = QHBoxLayout()
        search_field = QLineEdit()
        search_field.setPlaceholderText("Search roles...")
        search_field.setFixedHeight(40)
        search_field.setFont(self.predator_font)
        search_field.setStyleSheet(f"""
            QLineEdit {{
                background-color: #151A21;
                color: white;
                border: 1px solid #00B0C8;
                border-radius: 5px;
                padding: 5px;
                font-family: '{self.predator_font.family()}';
            }}
            QLineEdit:focus {{
                border: 2px solid #00B0C8;
            }}
        """)
        search_layout.addWidget(search_field)
        search_widget = QWidget()
        search_widget.setLayout(search_layout)
        self.internal_window.layout().addWidget(search_widget)

        # Update roles repo (git pull)
        repo_dir = os.path.expanduser("~/.config/exodia-roles-management/Exodia-OS-Roles")
        update_label = QLabel("Updating roles repo...")
        update_label.setFont(self.predator_font)
        update_label.setStyleSheet("color: #00B0C8; font-size: 16px;")
        self.internal_window.layout().addWidget(update_label)
        QApplication.processEvents()
        try:
            pull_proc = subprocess.run(["git", "pull"], cwd=repo_dir, capture_output=True, text=True)
            if pull_proc.returncode == 0:
                update_label.setText("Roles repo updated.")
            else:
                update_label.setText(f"Failed to update roles repo: {pull_proc.stderr}")
        except Exception as e:
            update_label.setText(f"Error updating roles repo: {str(e)}")
        QApplication.processEvents()
        time.sleep(0.5)
        update_label.hide()

        # List roles
        all_roles = roles_utils.get_all_repo_roles()
        installed_roles = set(roles_utils.get_available_roles())
        search_text = ""

        def refresh_roles():
            # Remove previous roles grid if exists
            for i in reversed(range(self.internal_window.layout().count())):
                item = self.internal_window.layout().itemAt(i)
                widget = item.widget()
                if isinstance(widget, QScrollArea) or isinstance(widget, QWidget) and widget.objectName() == "roles_splitter":
                    widget.deleteLater()
            # Splitter layout
            splitter = QWidget()
            splitter.setObjectName("roles_splitter")
            splitter_layout = QHBoxLayout(splitter)
            splitter_layout.setContentsMargins(0, 0, 0, 0)
            splitter_layout.setSpacing(20)
            # Helper to create a side (official/community)
            def create_side(title, roles_list, source_type):
                side_widget = QWidget()
                side_widget.setStyleSheet("background-color: #0E1218;")
                vbox = QVBoxLayout(side_widget)
                vbox.setContentsMargins(10, 10, 10, 10)
                vbox.setSpacing(10)
                title_label = QLabel(title)
                title_label.setFont(self.predator_font)
                title_label.setStyleSheet(f"color: #00B0C8; font-size: 20px; font-family: '{self.predator_font.family()}';")
                title_label.setAlignment(Qt.AlignCenter)
                vbox.addWidget(title_label)
                scroll_area = QScrollArea()
                scroll_area.setWidgetResizable(True)
                scroll_area.setStyleSheet("""
                    QScrollArea { border: none; background-color: #0E1218; }
                    QScrollBar:vertical { background: #151A21; width: 10px; }
                    QScrollBar::handle:vertical { background: #00B0C8; border-radius: 0px; }
                    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { background: #00B0C8; }
                    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: #151A21; }
                """)
                scroll_content = QWidget()
                grid = QGridLayout(scroll_content)
                grid.setContentsMargins(10, 10, 10, 10)
                grid.setSpacing(15)
                row = 0
                col = 0
                for role_name in roles_list:
                    container = QFrame()
                    container.setStyleSheet("background-color: #151A21; border-radius: 8px; border: 1px solid #00B0C8;")
                    vbox2 = QVBoxLayout(container)
                    vbox2.setAlignment(Qt.AlignTop)
                    label = QLabel(f"{role_name}")
                    label.setFont(self.predator_font)
                    label.setStyleSheet(f"color: #00B0C8; font-size: 18px; font-family: '{self.predator_font.family()}';")
                    label.setAlignment(Qt.AlignCenter)
                    vbox2.addWidget(label)
                    status = QLabel()
                    status.setFont(self.predator_font)
                    status.setAlignment(Qt.AlignCenter)
                    if role_name in installed_roles:
                        status.setText("Installed")
                        status.setStyleSheet("color: #00C8B0; font-size: 16px;")
                    else:
                        status.setText("Not Installed")
                        status.setStyleSheet("color: #B0B8C8; font-size: 16px;")
                    vbox2.addWidget(status)
                    btn = QPushButton()
                    btn.setFont(self.predator_font)
                    btn.setFixedHeight(40)
                    if role_name in installed_roles:
                        btn.setText("Uninstall")
                        btn.setStyleSheet("background-color: #B00020; color: white; border-radius: 5px; font-size: 16px;")
                        def uninstall_role(role=role_name):
                            ok, msg = roles_utils.remove_role(role)
                            if ok:
                                installed_roles.discard(role)
                                # Check if the uninstalled role was the currently selected one
                                current_selected = roles_utils.load_role_from_yaml()
                                if current_selected == role:
                                    # Clear the role selection by setting it to null
                                    roles_utils.clear_role_selection()
                                refresh_roles()
                            else:
                                QMessageBox.critical(container, "Uninstall Failed", f"Failed to uninstall role: {msg}")
                        btn.clicked.connect(lambda _, role=role_name: uninstall_role(role))
                    else:
                        btn.setText("Install")
                        btn.setStyleSheet("background-color: #00B0C8; color: white; border-radius: 5px; font-size: 16px;")
                        def install_role(role=role_name, source=source_type):
                            ok, msg = roles_utils.update_role_from_system(role, source)
                            if ok:
                                installed_roles.add(role)
                                refresh_roles()
                            else:
                                QMessageBox.critical(container, "Install Failed", f"Failed to install role: {msg}")
                        btn.clicked.connect(lambda _, role=role_name, source=source_type: install_role(role, source))
                    vbox2.addWidget(btn)
                    grid.addWidget(container, row, col)
                    col += 1
                    if col >= 1:
                        col = 0
                        row += 1
                scroll_area.setWidget(scroll_content)
                vbox.addWidget(scroll_area)
                return side_widget
            # Filtered roles
            filtered_official = [r for r in all_roles['official'] if search_text.lower() in r.lower()]
            filtered_community = [r for r in all_roles['community'] if search_text.lower() in r.lower()]
            # Add both sides
            splitter_layout.addWidget(create_side("Official Roles", filtered_official, "official"))
            splitter_layout.addWidget(create_side("Community Roles", filtered_community, "community"))
            self.internal_window.layout().addWidget(splitter)
        def on_search():
            nonlocal search_text
            search_text = search_field.text()
            refresh_roles()
        search_field.textChanged.connect(on_search)
        refresh_roles()

    def display_manage_role(self, back_callback=None):
        """
        Display the "Manage Your Role" content with a Back button and a tabbed interface
        with three tabs: Roadmap, Materials, and Setup Environment.

        Args:
            back_callback (function): Callback function to execute when the Back button is clicked
        """
        # Store the callback for later use (for UI refreshes)
        self.back_callback = back_callback
        # Clear the existing layout
        if not self.internal_window.layout():
            self.internal_window.setLayout(QVBoxLayout())

        # Clear previous content
        while self.internal_window.layout().count():
            item = self.internal_window.layout().takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # Create a "Back" button to return to the roles view
        back_button = QPushButton("Back")
        back_button.setFont(self.predator_font)
        back_button.setFixedSize(100, 40)
        back_button.setStyleSheet(
            """
            QPushButton {
                background-color: #006C7A;
                color: white;
                border: none;
                font-size: 18px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #004F59;
            }
            QPushButton:pressed {
                background-color: #005F78;
            }
            """
        )

        # Connect the Back button to the callback function or a default function
        if back_callback:
            back_button.clicked.connect(back_callback)
        else:
            # Default behavior if no callback is provided
            back_button.clicked.connect(lambda: self.internal_window.setLayout(QVBoxLayout()))

        # Add the "Back" button to the top layout
        top_layout = QHBoxLayout()
        top_layout.addWidget(back_button, alignment=Qt.AlignLeft)

        # Add a title label
        selected_role = roles_utils.load_role_from_yaml()
        title_label = QLabel(f"Manage Your {selected_role} Role")
        title_label.setFont(self.predator_font)
        title_label.setStyleSheet(
            f"color: #00B0C8; font-size: 24px; font-weight: bold; font-family: '{self.predator_font.family()}';"
        )
        title_label.setAlignment(Qt.AlignCenter)
        top_layout.addWidget(title_label, alignment=Qt.AlignCenter)

        # Add a spacer to balance the layout
        spacer = QWidget()
        spacer.setFixedSize(100, 40)
        top_layout.addWidget(spacer, alignment=Qt.AlignRight)

        top_widget = QWidget()
        top_widget.setLayout(top_layout)
        self.internal_window.layout().addWidget(top_widget)

        # Create a tab widget
        tab_widget = QTabWidget()
        font_family = self.predator_font.family()
        tab_widget.setStyleSheet(f"""
            QTabWidget::pane {{
                border: 1px solid #00B0C8;
                background-color: #151A21;
                border-radius: 5px;
            }}
            QTabBar::tab {{
                background-color: #151A21;
                color: #00B0C8;
                padding: 8px 20px;
                margin-right: 2px;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
                font-family: '{font_family}';
                font-size: 16px;
                min-width: 150px;
                text-align: center;
            }}
            QTabBar::tab:selected {{
                background-color: #00B0C8;
                color: white;
            }}
        """)

        # Create tabs
        self.create_roadmap_tab(tab_widget)
        self.create_materials_tab(tab_widget)
        self.create_hands_on_tab(tab_widget)
        create_setup_environment_tab(self, tab_widget)

        # Add the tab widget to the layout
        self.internal_window.layout().addWidget(tab_widget)

    def create_roadmap_tab(self, tab_widget):
        """
        Create the Roadmap tab content.

        Args:
            tab_widget (QTabWidget): The tab widget to add the tab to
        """
        roadmap_tab = QWidget()
        roadmap_tab.setStyleSheet("background-color: #151A21;")
        roadmap_layout = QVBoxLayout(roadmap_tab)
        roadmap_layout.setAlignment(Qt.AlignTop)
        roadmap_layout.setContentsMargins(20, 20, 20, 20)
        roadmap_layout.setSpacing(15)

        # Add title
        title_label = QLabel("Role Roadmap")
        title_label.setFont(self.predator_font)
        font_family = self.predator_font.family()
        title_label.setStyleSheet(f"color: #00B0C8; font-family: '{font_family}'; font-size: 24px;")
        roadmap_layout.addWidget(title_label)

        # Add separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("background-color: #00B0C8;")
        roadmap_layout.addWidget(separator)

        # Add content
        content_label = QTextBrowser()
        content_label.setOpenExternalLinks(True)
        content_label.setOpenLinks(False)  # We'll handle link clicks ourselves
        content_label.setTextInteractionFlags(Qt.TextSelectableByMouse | Qt.LinksAccessibleByMouse)
        content_label.anchorClicked.connect(open_url)

        # Style the QTextBrowser to match the QLabel styling
        content_label.setStyleSheet(f"color: #00B0C8; font-size: 18px; background-color: #151A21; padding: 10px; font-family: '{font_family}'; border: none;")

        # Get the selected role from role.yaml
        selected_role = roles_utils.load_role_from_yaml()

        if selected_role:
            # Construct the path to the roadmap.html file for the selected role
            # config_dir = os.path.expanduser("~/.config/exodia-assistant")
            # os.makedirs(config_dir, exist_ok=True)  # Ensure directory exists
            roadmap_path = os.path.join(ROLES_PROFILES_DIR, f"{selected_role}/roadmap.html")
            # print(roadmap_path)

            # Check if the roadmap.html file exists
            if os.path.exists(roadmap_path):
                # Load the HTML content from the file
                with open(roadmap_path, "r", encoding="utf-8") as html_file:
                    html_content = html_file.read()

                # Expand ~ in image paths to a full home path
                home_dir = os.path.expanduser("~")
                html_content = html_content.replace('src="~', f'src="file://{home_dir}')
                html_content = html_content.replace("src='~", f"src='file://{home_dir}")

                content_label.setText(html_content)
            else:
                # Display an error message if the file doesn't exist
                content_label.setText(f"""
                <div style="color: #00B0C8; line-height: 1.6; font-size: 18px; font-family: {font_family};">
                    <p>Roadmap file not found for the selected role: {selected_role}</p>
                    <p>Expected path: {roadmap_path}</p>
                </div>
                """)
        else:
            # Display a message if no role is selected
            content_label.setText(f"""
            <div style="color: #00B0C8; line-height: 1.6; font-size: 18px; font-family: {font_family};">
                <p>This tab displays the roadmap for your selected role, including:</p>
                <ul>
                    <li>Learning path</li>
                    <li>Skill progression</li>
                    <li>Career milestones</li>
                    <li>Certification recommendations</li>
                </ul>
                <p>Select a role to view its specific roadmap.</p>
            </div>
            """)

        content_label.setStyleSheet(f"color: #00B0C8; font-size: 18px; font-family: '{font_family}';")
        roadmap_layout.addWidget(content_label)

        # Create a scroll area for the content
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(roadmap_tab)
        scroll_area.setStyleSheet("""
            QScrollArea { 
                border: none;
                background-color: #151A21;
            }
            QScrollBar:vertical {
                background: #151A21;
                width: 10px;
                margin: 0;
            }
            QScrollBar::handle:vertical {
                background: #00B0C8;
                border-radius: 0px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background: #00B0C8;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: #151A21;
            }
        """)

        # Add the tab to the tab widget
        tab_widget.addTab(scroll_area, "Roadmap")

    def create_materials_tab(self, tab_widget):
        """
        Create the Materials tab content.

        Args:
            tab_widget (QTabWidget): The tab widget to add the tab to
        """
        materials_tab = QWidget()
        materials_tab.setStyleSheet("background-color: #151A21;")
        materials_layout = QVBoxLayout(materials_tab)
        materials_layout.setAlignment(Qt.AlignTop)
        materials_layout.setContentsMargins(20, 20, 20, 20)
        materials_layout.setSpacing(15)

        # Add title
        title_label = QLabel("Learning Materials")
        title_label.setFont(self.predator_font)
        font_family = self.predator_font.family()
        title_label.setStyleSheet(f"color: #00B0C8; font-family: '{font_family}'; font-size: 24px;")
        materials_layout.addWidget(title_label)

        # Add separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("background-color: #00B0C8;")
        materials_layout.addWidget(separator)

        # Add content
        content_label = QTextBrowser()
        content_label.setOpenExternalLinks(True)
        content_label.setOpenLinks(False)  # We'll handle link clicks ourselves
        content_label.setTextInteractionFlags(Qt.TextSelectableByMouse | Qt.LinksAccessibleByMouse)
        content_label.anchorClicked.connect(open_url)

        # Style the QTextBrowser to match the QLabel styling
        content_label.setStyleSheet(f"color: #00B0C8; font-size: 18px; background-color: #151A21; padding: 10px; font-family: '{font_family}'; border: none;")

        # Get the selected role from role.yaml
        selected_role = roles_utils.load_role_from_yaml()

        if selected_role:
            # Construct the path to the materials.html file for the selected role
            # config_dir = os.path.expanduser("~/.config/exodia-assistant")
            # os.makedirs(config_dir, exist_ok=True)  # Ensure directory exists
            materials_html_path = os.path.join(ROLES_PROFILES_DIR, f"{selected_role}/materials.html")
            materials_md_path = os.path.join(ROLES_PROFILES_DIR, f"{selected_role}/materials.md")
            # print(materials_html_path)
            # print(materials_md_path)

            # Check if the materials.html file exists
            if os.path.exists(materials_html_path):
                # Load the HTML content from the file
                with open(materials_html_path, "r", encoding="utf-8") as html_file:
                    html_content = html_file.read()
                content_label.setText(html_content)
            # Check if the materials.md file exists
            elif os.path.exists(materials_md_path):
                # Load the MD content from the file
                with open(materials_md_path, "r", encoding="utf-8") as md_file:
                    md_content = md_file.read()
                # Convert MD content to HTML (simple conversion for display)
                html_content = f"""
                <div style="color: #00B0C8; line-height: 1.6; font-size: 18px; font-family: {font_family};">
                    {md_content}
                </div>
                """
                content_label.setText(html_content)
            else:
                # Display an error message if neither file exists
                content_label.setText(f"""
                <div style="color: #00B0C8; line-height: 1.6; font-size: 18px; font-family: {font_family};">
                    <p>Materials file not found for the selected role: {selected_role}</p>
                    <p>Expected paths:</p>
                    <p>{materials_html_path}</p>
                    <p>or</p>
                    <p>{materials_md_path}</p>
                </div>
                """)
        else:
            # Display a message if no role is selected
            content_label.setText(f"""
            <div style="color: #00B0C8; line-height: 1.6; font-size: 18px; font-family: {font_family};">
                <p>This tab provides learning materials for your selected role, including:</p>
                <ul>
                    <li>Books and publications</li>
                    <li>Online courses</li>
                    <li>Video tutorials</li>
                    <li>Documentation and references</li>
                    <li>Practice exercises</li>
                </ul>
                <p>Select a role to view its specific learning materials.</p>
            </div>
            """)

        content_label.setStyleSheet(f"color: #00B0C8; font-size: 18px; font-family: '{font_family}';")
        materials_layout.addWidget(content_label)

        # Create a scroll area for the content
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(materials_tab)
        scroll_area.setStyleSheet("""
            QScrollArea { 
                border: none;
                background-color: #151A21;
            }
            QScrollBar:vertical {
                background: #151A21;
                width: 10px;
                margin: 0;
            }
            QScrollBar::handle:vertical {
                background: #00B0C8;
                border-radius: 0px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background: #00B0C8;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: #151A21;
            }
        """)

        # Add the tab to the tab widget
        tab_widget.addTab(scroll_area, "Materials")

    def create_hands_on_tab(self, tab_widget):
        """
        Create the Hands-On tab content.

        Args:
            tab_widget (QTabWidget): The tab widget to add the tab to
        """
        hands_on_tab = QWidget()
        hands_on_tab.setStyleSheet("background-color: #151A21;")
        hands_on_layout = QVBoxLayout(hands_on_tab)
        hands_on_layout.setAlignment(Qt.AlignTop)
        hands_on_layout.setContentsMargins(20, 20, 20, 20)
        hands_on_layout.setSpacing(15)

        # Add title
        title_label = QLabel("Now, Let's get our hands dirty!")
        title_label.setFont(self.predator_font)
        font_family = self.predator_font.family()
        title_label.setStyleSheet(f"color: #00B0C8; font-family: '{font_family}'; font-size: 24px;")
        hands_on_layout.addWidget(title_label)

        # Add separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("background-color: #00B0C8;")
        hands_on_layout.addWidget(separator)

        # Add content
        content_label = QTextBrowser()
        content_label.setOpenExternalLinks(True)
        content_label.setOpenLinks(False)  # We'll handle link clicks ourselves
        content_label.setTextInteractionFlags(Qt.TextSelectableByMouse | Qt.LinksAccessibleByMouse)
        content_label.anchorClicked.connect(open_url)
        content_label.setStyleSheet(f"color: #00B0C8; font-size: 18px; background-color: #151A21; padding: 10px; font-family: '{font_family}'; border: none;")

        # Get the selected role from role.yaml
        selected_role = roles_utils.load_role_from_yaml()

        if selected_role:
            hands_on_html_path = os.path.join(ROLES_PROFILES_DIR, f"{selected_role}/hands_on.html")
            if os.path.exists(hands_on_html_path):
                with open(hands_on_html_path, "r", encoding="utf-8") as html_file:
                    html_content = html_file.read()
                content_label.setText(html_content)
            else:
                content_label.setText(f"""
                <div style="color: #00B0C8; line-height: 1.6; font-size: 18px; font-family: {font_family};">
                    <p>No hands-on exercises or practice content found for the selected role: {selected_role}</p>
                    <p>Expected path: {hands_on_html_path}</p>
                </div>
                """)
        else:
            content_label.setText(f"""
            <div style="color: #00B0C8; line-height: 1.6; font-size: 18px; font-family: {font_family};">
                <p>This tab provides hands-on exercises and practice for your selected role, including:</p>
                <ul>
                    <li>Practical coding tasks</li>
                    <li>Mini-projects</li>
                    <li>Quizzes and challenges</li>
                    <li>Step-by-step guides</li>
                </ul>
                <p>Select a role to view its specific hands-on content.</p>
            </div>
            """)

        content_label.setStyleSheet(f"color: #00B0C8; font-size: 18px; font-family: '{font_family}';")
        hands_on_layout.addWidget(content_label)

        # Create a scroll area for the content
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(hands_on_tab)
        scroll_area.setStyleSheet("""
            QScrollArea { 
                border: none;
                background-color: #151A21;
            }
            QScrollBar:vertical {
                background: #151A21;
                width: 10px;
                margin: 0;
            }
            QScrollBar::handle:vertical {
                background: #00B0C8;
                border-radius: 0px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background: #00B0C8;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: #151A21;
            }
        """)

        # Add the tab to the tab widget
        tab_widget.addTab(scroll_area, "Hands-On")

    def show_role_selection_window(self):
        """
        Show the role selection window.
        Creates a new window each time to ensure it's up to date.
        """
        # Always create a new window to ensure it's up to date
        self.role_selection_window = roles_utils.RoleSelectionWindow(predator_font=self.predator_font)
        self.role_selection_window.show()