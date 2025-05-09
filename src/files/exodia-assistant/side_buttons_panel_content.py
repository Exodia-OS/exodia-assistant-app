#####################################
#                                   #
#  @author      : 00xWolf           #
#    GitHub    : @mmsaeed509       #
#    Developer : Mahmoud Mohamed   #
#  﫥  Copyright : Exodia OS         #
#                                   #
#####################################

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QScrollArea, QLineEdit, QFrame
import utils
from roles.role import Role
import keybinding, wiki
from news import News
from tweaks import Tweaks
from PyQt5.QtCore import Qt

class ButtonContent:

    def __init__(self, internal_window):
        self.internal_window = internal_window
        self.predator_font = utils.loadPredatorFont()

    def clearButtons(self):
        # Remove all button widgets from the internal window
        for i in reversed(range(self.internal_window.layout().count())):
            widget = self.internal_window.layout().itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

    def displayWelcomeContent(self):
        # Clear previous buttons
        self.clearButtons()
        # Load and format the HTML content
        text = utils.loadHTMLContent('./HTML-files', 'displayWelcomeContent.html', self.predator_font.family())

        # Update the content of the internal window
        self.internal_window.updateContent(text)

    def displayDevelopersContent(self):

        self.clearButtons()  # Clear previous buttons
        # Load and format the HTML content
        text = utils.loadHTMLContent('./HTML-files', 'displayDevelopersContent.html', self.predator_font.family())
        # Update the content of the internal window
        self.internal_window.updateContent(text)

    def displayTweaksContent(self):

        # Clear previous buttons
        if not self.internal_window.layout():
            self.internal_window.setLayout(QVBoxLayout())
            self.clearButtons()
        else:
            self.clearButtons()

        # Create an instance of the Tweaks class
        tweaks = Tweaks()

        # Call the display_tweaks method to display tweaks content
        tweaks.display_tweaks(self.internal_window)

    def displayNewsContent(self):

        # Clear previous buttons
        if not self.internal_window.layout():
            self.internal_window.setLayout(QVBoxLayout())
            self.clearButtons()
        else:
            self.clearButtons()

        # Create an instance of the News class
        news = News()

        # Call the fetch_and_display_news method to fetch and display news content
        news.fetch_and_display_news(self.internal_window)

    def displayRoleContent(self):

        self.clearButtons()  # Clear previous buttons

        # Create an instance of the Role class
        role = Role()

        # Load the role content (index page by default)
        role_content = role.load_role_content()

        # Update the content of the internal window
        self.internal_window.updateContent(role_content)

        # Add buttons for each available role
        def create_role_buttons():
            # Create a container for the buttons
            buttons_container = QWidget()
            buttons_layout = QHBoxLayout(buttons_container)
            buttons_layout.setContentsMargins(20, 20, 20, 20)
            buttons_layout.setSpacing(20)

            # Create a button for each available role
            for role_name in role.get_available_roles():
                role_button = QPushButton()
                role_button.setFixedSize(240, 100)
                role_button.setMask(utils.contentButtonMask())
                role_button.setStyleSheet("""
                    QPushButton {
                        background-color: #00B0C8;
                        color: white;
                        border: none;
                    }
                    QPushButton:hover {
                        background-color: #0086A8;
                    }
                    QPushButton:pressed {
                        background-color: #005F78;
                    }
                """)

                # Create a label for the button text with predator font
                text_label = QLabel(role_name)
                text_label.setAlignment(Qt.AlignCenter)
                text_label.setWordWrap(True)
                text_label.setStyleSheet(
                    f"color: white; font-family: '{self.predator_font.family()}'; font-size: 18px;"
                )

                # Add the label to the button
                button_layout = QVBoxLayout()
                button_layout.addWidget(text_label)
                button_layout.setContentsMargins(0, 0, 0, 0)
                role_button.setLayout(button_layout)

                # Connect the button to a function that loads the role content or shows the role selection window
                if role_name == "Select a Role":
                    role_button.clicked.connect(self.show_role_selection)
                else:
                    role_button.clicked.connect(lambda checked, name=role_name: self.load_specific_role(name))

                # Add the button to the layout
                buttons_layout.addWidget(role_button)

            # Add the button container to the internal window
            self.internal_window.layout().addWidget(buttons_container)

        # Create the role buttons
        create_role_buttons()

    def load_specific_role(self, role_name):
        """
        Load the content for a specific role

        Args:
            role_name (str): The name of the role to load
        """
        self.clearButtons()  # Clear previous buttons

        # Create an instance of the Role class
        role = Role()

        # For "Create a Role" or "Manage Your Role", pass the internal_window and back_callback to enable the new display method
        if role_name == "Create a Role" or role_name == "Manage Your Role" or role_name == "How to Create Your Own Role":
            # Load the role content with the internal window and back_callback
            role_content = role.load_role_content(role_name, self.internal_window, self.displayRoleContent)

            # If content is empty, it means the display_create_role or display_manage_role method handled the display
            if not role_content:
                # Clear the content of the internal window before returning
                self.internal_window.updateContent("")
                return

            # Otherwise, update the content of the internal window
            self.internal_window.updateContent(role_content)
        else:
            # Load the role content for other roles
            role_content = role.load_role_content(role_name)

            # Update the content of the internal window
            self.internal_window.updateContent(role_content)

            # Add a back button
            back_button = QPushButton()
            back_button.setFixedSize(240, 100)
            back_button.setMask(utils.contentButtonMask())
            back_button.setStyleSheet("""
                QPushButton {
                    background-color: #00B0C8;
                    color: white;
                    border: none;
                }
                QPushButton:hover {
                    background-color: #0086A8;
                }
                QPushButton:pressed {
                    background-color: #005F78;
                }
            """)

            # Create a label for the button text with predator font
            text_label = QLabel("Back")
            text_label.setAlignment(Qt.AlignCenter)
            text_label.setWordWrap(True)
            text_label.setStyleSheet(
                f"color: white; font-family: '{self.predator_font.family()}'; font-size: 18px;"
            )

            # Add the label to the button
            button_layout = QVBoxLayout()
            button_layout.addWidget(text_label)
            button_layout.setContentsMargins(0, 0, 0, 0)
            back_button.setLayout(button_layout)

            back_button.clicked.connect(self.displayRoleContent)

            # Add the back button to the internal window
            self.internal_window.layout().addWidget(back_button)

    def displayKeybindingContent(self):
        keybinding.displayKeybindingContent(self.internal_window, self.predator_font)

    def displayWikiContent(self):
        wiki.displayWikiContent(self.internal_window, self.predator_font)

    def show_role_selection(self):
        """
        Show the role selection window.
        """
        role = Role()
        role.show_role_selection_window()
