#####################################
#                                   #
#  @author      : 00xWolf           #
#    GitHub    : @mmsaeed509       #
#    Developer : Mahmoud Mohamed   #
#  﫥  Copyright : Exodia OS         #
#                                   #
#####################################

import os, sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QPushButton, QLabel, QHBoxLayout, QTabWidget, QFrame, QTextBrowser
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDesktopServices
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utils
from . import roles_utils


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

        # Use predator font from utils.py
        self.predator_font = None
        self.predator_font = utils.loadPredatorFont()
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
        config_dir = os.path.expanduser("~/.config/exodia-assistant")
        os.makedirs(config_dir, exist_ok=True)  # Ensure directory exists
        roles_dir = os.path.join(config_dir, "/profiles")

        text = """<div style="font-family: {}; color: #00B0C8; line-height: 1.6; font-size: 18px; max-width: 800px; margin: auto; padding: 0 20px;">                    
                    <h4 style="color: #00C8B0; font-size: 20px; margin-bottom: 15px;"> Role Overview </h4>
                </div>""".format(self.predator_font.family())

        # If no role is specified, load the index page
        if role_name is None or role_name not in self.roles:
            # return text
            return utils.loadHTMLContent('./HTML-files', 'displayRoleContent.html', self.predator_font.family())

        # If the role is "Select a Role", show the role selection window
        elif role_name == "Select a Role":
            self.show_role_selection_window()
            return utils.loadHTMLContent('./HTML-files', 'displayRoleContent.html', self.predator_font.family())

        # If the role is "Create a Role", use the display_create_role method if internal_window is available
        elif role_name == "Create a Role":
            if self.internal_window:
                self.display_create_role(back_callback)
                return ""  # Return empty string as content will be handled by display_create_role
            else:
                # Fallback to the old method if internal_window is not available
                return f"""<div style="font-family: {self.predator_font.family()}; color: #00B0C8; line-height: 1.6; font-size: 18px; max-width: 800px; margin: auto; padding: 0 20px;">
                    <h4 style="color: #00C8B0; font-size: 20px; margin-bottom: 15px;">{role_name}</h4>
                    <p>This category is under development. will be available soon!</p>
                </div>"""

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
        html_content = f"""
        <div style="color: #00B0C8; line-height: 1.6; font-size: 18px; max-width: 800px; margin: auto; padding: 0 20px; font-family: {self.predator_font.family()};">
          <h1 style="color: #00B0C8; font-size: 32px; margin-bottom: 20px; text-align: center;">Create a Role</h1>
          It's allows you to Create Your Own Role. and you can share this role with others.
          <p style="font-size: 20px; text-align: center;">
            This category is under development. will be available soon!
          </p>
        </div>
        """

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
        Display the "Explore Role" content with a Back button and scroll area
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

        # Create the content for the "Explore Role" section
        html_content = utils.loadHTMLContent('./HTML-files', 'ExploreRole.html', self.predator_font.family())

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

    def display_manage_role(self, back_callback=None):
        """
        Display the "Manage Your Role" content with a Back button and a tabbed interface
        with three tabs: Roadmap, Materials, and Setup Environment.

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

        # Add a title label
        selected_role = roles_utils.load_role_from_yaml() or "Default"
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
        self.create_setup_environment_tab(tab_widget)

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
            roadmap_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                       f"profiles/{selected_role}/roadmap.html")

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
            materials_html_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                       f"profiles/{selected_role}/materials.html")
            materials_md_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                       f"profiles/{selected_role}/materials.md")

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

    def create_setup_environment_tab(self, tab_widget):
        """
        Create the Setup Environment tab content.

        Args:
            tab_widget (QTabWidget): The tab widget to add the tab to
        """
        import subprocess
        import yaml
        import os

        setup_tab = QWidget()
        setup_tab.setStyleSheet("background-color: #151A21;")
        setup_layout = QVBoxLayout(setup_tab)
        setup_layout.setAlignment(Qt.AlignTop)
        setup_layout.setContentsMargins(20, 20, 20, 20)
        setup_layout.setSpacing(15)

        # Add title
        title_label = QLabel("Environment")
        title_label.setFont(self.predator_font)
        font_family = self.predator_font.family()
        title_label.setStyleSheet(f"color: #00B0C8; font-family: '{font_family}'; font-size: 24px;")
        setup_layout.addWidget(title_label)

        # Add separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("background-color: #00B0C8;")
        setup_layout.addWidget(separator)

        # Get the selected role from role.yaml
        selected_role = roles_utils.load_role_from_yaml()

        if not selected_role:
            # Display a message if no role is selected
            content_label = QTextBrowser()
            content_label.setOpenExternalLinks(True)
            content_label.setOpenLinks(False)
            content_label.setTextInteractionFlags(Qt.TextSelectableByMouse | Qt.LinksAccessibleByMouse)
            content_label.anchorClicked.connect(open_url)
            content_label.setStyleSheet(f"color: #00B0C8; font-size: 18px; background-color: #151A21; padding: 10px; font-family: '{font_family}'; border: none;")
            content_label.setText(f"""
            <div style="color: #00B0C8; line-height: 1.6; font-size: 18px; font-family: {font_family};">
                <p>This tab provides guidance on setting up your development environment for your selected role, including:</p>
                <ul>
                    <li>Required software and tools</li>
                    <li>Configuration instructions</li>
                    <li>Best practices</li>
                    <li>Recommended extensions and plugins</li>
                    <li>Environment troubleshooting</li>
                </ul>
                <p>Select a role to view its specific environment setup instructions.</p>
            </div>
            """)
            setup_layout.addWidget(content_label)
        else:
            # Construct the path to the tools.yaml file for the selected role
            config_dir = os.path.expanduser("~/.config/exodia-assistant")
            os.makedirs(config_dir, exist_ok=True)  # Ensure directory exists
            tools_path = os.path.join(config_dir, f"profiles/{selected_role}/tools.yaml")

            # Check if the tools.yaml file exists
            if not os.path.exists(tools_path):
                content_label = QTextBrowser()
                content_label.setStyleSheet(f"color: #00B0C8; font-size: 18px; background-color: #151A21; padding: 10px; font-family: '{font_family}'; border: none;")
                content_label.setText(f"""
                <div style="color: #00B0C8; line-height: 1.6; font-size: 18px; font-family: {font_family};">
                    <p>Tools configuration file not found for the selected role: {selected_role}</p>
                    <p>Expected path: {tools_path}</p>
                </div>
                """)
                setup_layout.addWidget(content_label)
            else:
                # Load the tools.yaml file
                try:
                    with open(tools_path, 'r') as file:
                        tools_data = yaml.safe_load(file)

                    # Function to check if a package is installed
                    def is_package_installed(package):
                        if package.startswith("bash "):
                            # For script-based installations, we can't easily check
                            return False
                        try:
                            # Try to check if the package is installed using pacman
                            result = subprocess.run(
                                ["pacman", "-Q", package.strip()], 
                                stdout=subprocess.PIPE, 
                                stderr=subprocess.PIPE,
                                text=True
                            )
                            return result.returncode == 0
                        except Exception:
                            return False

                    # Function to update the tools.yaml file
                    def update_tools_yaml():
                        with open(tools_path, 'w') as file:
                            yaml.dump(tools_data, file, default_flow_style=False)

                    # Function to install a tool
                    def install_tool(tool):
                        # Run pre-exec commands if they exist
                        if tool.get('pre-exec'):
                            pre_exec_commands = tool['pre-exec'].split(',') if tool['pre-exec'] else []
                            for cmd in pre_exec_commands:
                                cmd = cmd.strip()
                                if cmd:
                                    if cmd.startswith("bash "):
                                        # Execute as a script
                                        subprocess.run(cmd, shell=True)
                                    else:
                                        # Execute as a shell command
                                        subprocess.run(cmd, shell=True)

                        # Install the packages
                        pkgs = tool.get('pkgs', '')
                        if pkgs:
                            if pkgs.startswith("bash "):
                                # Execute as a script
                                subprocess.run(pkgs, shell=True)
                            else:
                                # Install packages using pacman
                                package_list = [pkg.strip() for pkg in pkgs.split(',')]
                                subprocess.run(["sudo", "pacman", "-S", "--noconfirm"] + package_list)

                        # Run post-exec commands if they exist
                        if tool.get('post-exec'):
                            post_exec_commands = tool['post-exec'].split(',') if tool['post-exec'] else []
                            for cmd in post_exec_commands:
                                cmd = cmd.strip()
                                if cmd:
                                    if cmd.startswith("bash "):
                                        # Execute as a script
                                        subprocess.run(cmd, shell=True)
                                    else:
                                        # Execute as a shell command
                                        subprocess.run(cmd, shell=True)

                        # Update the tool status
                        tool['Status'] = 'Installed'
                        update_tools_yaml()

                    # Function to uninstall a tool
                    def uninstall_tool(tool):
                        # Uninstall the packages
                        pkgs = tool.get('pkgs', '')
                        if pkgs and not pkgs.startswith("bash "):
                            # Only uninstall if it's a package, not a script
                            package_list = [pkg.strip() for pkg in pkgs.split(',')]
                            subprocess.run(["sudo", "pacman", "-R", "--noconfirm"] + package_list)

                        # Update the tool status
                        tool['Status'] = 'UnInstalled'
                        update_tools_yaml()

                    # Create a "Select All Tools" checkbox
                    select_all_checkbox = QPushButton("Select All Tools")
                    select_all_checkbox.setCheckable(True)
                    select_all_checkbox.setFont(self.predator_font)
                    select_all_checkbox.setStyleSheet(f"""
                        QPushButton {{
                            background-color: #151A21;
                            color: #00B0C8;
                            border: 1px solid #00B0C8;
                            border-radius: 5px;
                            padding: 5px;
                            font-family: '{font_family}';
                            text-align: left;
                            padding-left: 10px;
                        }}
                        QPushButton:checked {{
                            background-color: #00B0C8;
                            color: white;
                        }}
                    """)
                    setup_layout.addWidget(select_all_checkbox)

                    # Dictionary to store all checkboxes
                    all_checkboxes = {}
                    category_checkboxes = {}
                    tool_checkboxes = {}
                    category_tools_dict = {}

                    # Create checkboxes for each category and tool
                    for category, tools in tools_data.items():
                        # Create a category checkbox
                        category_checkbox = QPushButton(category)
                        category_checkbox.setCheckable(True)
                        category_checkbox.setFont(self.predator_font)
                        category_checkbox.setStyleSheet(f"""
                            QPushButton {{
                                background-color: #151A21;
                                color: #00B0C8;
                                border: 1px solid #00B0C8;
                                border-radius: 5px;
                                padding: 5px;
                                font-family: '{font_family}';
                                text-align: left;
                                padding-left: 10px;
                                margin-top: 10px;
                            }}
                            QPushButton:checked {{
                                background-color: #00B0C8;
                                color: white;
                            }}
                        """)
                        setup_layout.addWidget(category_checkbox)
                        category_checkboxes[category] = category_checkbox
                        all_checkboxes[category] = category_checkbox

                        # Create checkboxes for each tool in the category
                        category_tools_checkboxes = []
                        for tool in tools:
                            # Check if the tool is installed
                            if 'Status' not in tool or not tool['Status']:
                                # Auto-detect installation status
                                if 'pkgs' in tool and tool['pkgs']:
                                    if tool['pkgs'].startswith("bash "):
                                        # For script-based installations, we can't easily check
                                        tool['Status'] = 'UnInstalled'
                                    else:
                                        # Check if all packages are installed
                                        packages = [pkg.strip() for pkg in tool['pkgs'].split(',')]
                                        if all(is_package_installed(pkg) for pkg in packages):
                                            tool['Status'] = 'Installed'
                                        else:
                                            tool['Status'] = 'UnInstalled'
                                else:
                                    tool['Status'] = 'UnInstalled'

                                # Update the YAML file with the detected status
                                update_tools_yaml()

                            # Create a tool checkbox
                            tool_checkbox = QPushButton(tool['name'])
                            tool_checkbox.setCheckable(True)
                            tool_checkbox.setChecked(tool['Status'] == 'Installed')
                            tool_checkbox.setFont(self.predator_font)
                            tool_checkbox.setStyleSheet(f"""
                                QPushButton {{
                                    background-color: #151A21;
                                    color: #00B0C8;
                                    border: 1px solid #00B0C8;
                                    border-radius: 5px;
                                    padding: 5px;
                                    font-family: '{font_family}';
                                    text-align: left;
                                    padding-left: 20px;
                                    margin-left: 20px;
                                }}
                                QPushButton:checked {{
                                    background-color: #00B0C8;
                                    color: white;
                                }}
                            """)
                            setup_layout.addWidget(tool_checkbox)

                            # Store the tool data with the checkbox
                            tool_checkbox.tool_data = tool
                            tool_checkboxes[tool['name']] = tool_checkbox
                            all_checkboxes[tool['name']] = tool_checkbox
                            category_tools_checkboxes.append(tool_checkbox)

                            # Connect the checkbox to install/uninstall functions
                            def toggle_tool_state(checked, t=tool, checkbox=tool_checkbox):
                                if checked:
                                    # Install the tool
                                    install_tool(t)
                                    checkbox.setChecked(True)
                                else:
                                    # Uninstall the tool
                                    uninstall_tool(t)
                                    checkbox.setChecked(False)

                                # Update category checkboxes
                                for cat, tools_checkboxes in category_tools_dict.items():
                                    cat_checkbox = category_checkboxes[cat]
                                    cat_checkbox.setChecked(all(cb.isChecked() for cb in tools_checkboxes))

                                # Update the "Select All" checkbox
                                select_all_checkbox.setChecked(all(cb.isChecked() for cb in all_checkboxes.values()))

                            tool_checkbox.toggled.connect(toggle_tool_state)

                        # Store the category's tools checkboxes
                        category_tools_dict[category] = category_tools_checkboxes

                        # Connect the category checkbox to toggle all tools in the category
                        def toggle_category(checked, cat=category, tools_checkboxes=category_tools_checkboxes):
                            for checkbox in tools_checkboxes:
                                checkbox.setChecked(checked)

                        category_checkbox.toggled.connect(toggle_category)

                        # Set the initial state of the category checkbox
                        category_checkbox.setChecked(all(cb.isChecked() for cb in category_tools_checkboxes))

                    # Connect the "Select All" checkbox to toggle all tools
                    def toggle_all_tools(checked):
                        for checkbox in all_checkboxes.values():
                            checkbox.setChecked(checked)

                    select_all_checkbox.toggled.connect(toggle_all_tools)

                    # Set the initial state of the "Select All" checkbox
                    select_all_checkbox.setChecked(all(cb.isChecked() for cb in all_checkboxes.values()))

                except Exception as e:
                    content_label = QTextBrowser()
                    content_label.setStyleSheet(f"color: #00B0C8; font-size: 18px; background-color: #151A21; padding: 10px; font-family: '{font_family}'; border: none;")
                    content_label.setText(f"""
                    <div style="color: #00B0C8; line-height: 1.6; font-size: 18px; font-family: {font_family};">
                        <p>Error loading tools configuration: {str(e)}</p>
                    </div>
                    """)
                    setup_layout.addWidget(content_label)

        # Create a scroll area for the content
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(setup_tab)
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
        tab_widget.addTab(scroll_area, "Environment")

    def show_role_selection_window(self):
        """
        Show the role selection window.
        Creates a new window each time to ensure it's up to date.
        """
        # Always create a new window to ensure it's up to date
        self.role_selection_window = roles_utils.RoleSelectionWindow(predator_font=self.predator_font)
        self.role_selection_window.show()
