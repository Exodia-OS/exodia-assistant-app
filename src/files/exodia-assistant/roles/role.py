#####################################
#                                   #
#  @author      : 00xWolf           #
#    GitHub    : @mmsaeed509       #
#    Developer : Mahmoud Mohamed   #
#  﫥  Copyright : Exodia OS         #
#                                   #
#####################################

import os, sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea
from PyQt5.QtCore import Qt
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utils
from . import roles_utils

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
        self.roles = ["Select a Role", "Manage Your Role", "Create a Role"]

        # Role selection window
        self.role_selection_window = None

    def load_role_content(self, role_name=None):
        # Path to the profiles directory
        roles_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "profiles")

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

    def show_role_selection_window(self):
        """
        Show the role selection window.
        Creates a new window each time to ensure it's up to date.
        """
        # Always create a new window to ensure it's up to date
        self.role_selection_window = roles_utils.RoleSelectionWindow(predator_font=self.predator_font)
        self.role_selection_window.show()
