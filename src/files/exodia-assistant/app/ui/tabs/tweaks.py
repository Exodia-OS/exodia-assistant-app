#####################################
#                                   #
#  @author      : 00xWolf           #
#    GitHub    : @mmsaeed509       #
#    Developer : Mahmoud Mohamed   #
#  﫥  Copyright : Exodia OS         #
#                                   #
#####################################

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QScrollArea, QLineEdit, QFrame
from PyQt5.QtCore import Qt
from ...utils import font_utils, html_utils, ui_utils

class Tweaks(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Set the geometry (position and size) of the widget
        self.internal_window = None
        self.setGeometry(0, 0, 800, 600)
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

        # use predator font
        self.scroll_area.setFont(self.predator_font)

        # Add the scroll area to the main layout
        self.layout.addWidget(self.scroll_area)

        # Available tweak categories
        self.categories = [
            "Change Themes",
            "Change Icons",
            "Change Cursors",
            "Change Polybar Theme",
            "Change RGB Keyboard",
            "Picom Configs",
            "Keybindings",
            "BSPWM Tweaks",
            "DWM Tweaks",
            "I3WM Tweaks",
            "Hyprland Tweaks",
            "Install WMs Themes",
            "Install WCs Themes"
        ]

    def display_tweaks(self, internal_window):

        self.internal_window = internal_window

        # Initialize the layout if needed
        if not self.internal_window.layout():
            self.internal_window.setLayout(QVBoxLayout())

        text = ""
        # HTML file for tweaks overview
        html_file = "displayTweaksContent.html"

        def clearLayout():
            """Clears the layout of the internal window."""
            while self.internal_window.layout().count():
                item = self.internal_window.layout().takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()

        def createCustomButton(label, category):
            """Creates a custom button widget with word-wrapped text and a custom shape."""
            button = QPushButton()
            button.setFixedSize(240, 100)
            button.setMask(ui_utils.contentButtonMask())
            button.setStyleSheet(
                f"""
                QPushButton {{
                    background-color: #00B0C8;
                    color: white;
                    border: none;
                }}
                QPushButton:hover {{
                    background-color: #00B0C8;
                }}
                QPushButton:pressed {{
                    background-color: #005F78;
                }}
                """
            )

            text_label = QLabel(label)
            text_label.setAlignment(Qt.AlignCenter)
            text_label.setWordWrap(True)
            # Adjust font size based on text length to ensure it fits
            font_size = 18 if len(label) < 20 else 16
            text_label.setStyleSheet(
                f"color: white; font-family: '{self.predator_font.family()}'; font-size: {font_size}px;"
            )

            layout = QVBoxLayout()
            layout.addWidget(text_label)
            layout.setContentsMargins(0, 0, 0, 0)
            button.setLayout(layout)

            button.clicked.connect(lambda _, cat=category: showCategory(cat))
            return button

        def showButtons(keyword=None):
            """Displays the main category buttons filtered by keyword."""
            clearLayout()

            # Create the search input field
            search_input = QLineEdit()
            search_input.setPlaceholderText("Tweaks Search...")
            search_input.setFixedHeight(40)
            search_input.setStyleSheet(
                """
                QLineEdit {
                    font-size: 18px;
                    font-family: Arial;
                    color: white;
                    background-color: #151A21;
                    padding: 5px;
                    border: 1px solid #00B0C8;
                    border-radius: 5px;
                }
                """
            )

            def performSearch():
                # Show buttons filtered by the search input
                keyword = search_input.text()
                showButtons(keyword)

            # Connect the "Enter" key press to the performSearch function
            search_input.returnPressed.connect(performSearch)

            # Add the search field
            top_layout = QHBoxLayout()
            top_layout.addWidget(search_input, alignment=Qt.AlignLeft)

            top_widget = QWidget()
            top_widget.setLayout(top_layout)
            self.internal_window.layout().addWidget(top_widget)

            # Filter the categories if a keyword is provided
            filtered_categories = self.categories
            if keyword:
                filtered_categories = [cat for cat in self.categories if keyword.lower() in cat.lower()]

            # Create a scrollable widget
            scroll_widget = QWidget()
            scroll_widget.setStyleSheet("background: transparent;")
            scroll_layout = QVBoxLayout(scroll_widget)
            scroll_layout.setContentsMargins(0, 0, 0, 0)

            # Add buttons to the scrollable widget in a grid layout
            row_layout = None
            for index, category in enumerate(filtered_categories):
                if index % 4 == 0:
                    row_layout = QHBoxLayout()
                    row_layout.setContentsMargins(0, 0, 0, 0)
                    scroll_layout.addLayout(row_layout)

                button = createCustomButton(category, category)
                row_layout.addWidget(button)

            # Add the scrollable widget to a scroll area
            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)
            scroll_area.setWidget(scroll_widget)
            scroll_area.setStyleSheet("""
                QScrollArea {
                    background: transparent;
                    border: none;
                }
                QScrollBar:vertical {
                    background: transparent;
                    width: 10px;
                    margin: 0 0 0 0;
                }
                QScrollBar::handle:vertical {
                    background: #00B0C8;
                    border-radius: 0px;
                }
                QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                    background: transparent;
                }
                QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                    background: transparent;
                }
            """)

            # Add the scroll area to the internal window
            self.internal_window.layout().addWidget(scroll_area)

            # Load the overview HTML content
            try:
                html_content = html_utils.loadHTMLContent("html", html_file, self.predator_font.family())
                # self.internal_window.updateContent(html_content)
            except Exception as e:
                print(f"Error loading HTML content: {e}")

        def showCategory(category):
            """Displays the content for a specific category."""
            try:
                # Clear the existing layout
                clearLayout()

                # Create a "Back" button to return to the buttons view
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
                back_button.clicked.connect(showButtons)

                # Add the "Back" button to the top layout
                top_layout = QHBoxLayout()
                top_layout.addWidget(back_button, alignment=Qt.AlignLeft)

                top_widget = QWidget()
                top_widget.setLayout(top_layout)
                self.internal_window.layout().addWidget(top_widget)

                # Display a placeholder message for now
                html_content = f"""
                <div style="color: #00B0C8; line-height: 1.6; font-size: 18px; max-width: 800px; margin: auto; padding: 0 20px; font-family: {self.predator_font.family()};">
                  <h1 style="color: #00B0C8; font-size: 32px; margin-bottom: 20px; text-align: center;">{category}</h1>

                  <p style="font-size: 20px; text-align: center;">
                    This category is under development. More features will be available soon!
                  </p>
                </div>
                """

                # Use the scroll area from the internal window
                content_label = QLabel()
                content_label.setTextFormat(Qt.RichText)
                content_label.setWordWrap(True)
                content_label.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
                content_label.setText(html_content)

                scroll_area = QScrollArea()
                scroll_area.setGeometry(40, 20, 1100, 600)
                scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
                scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
                scroll_area.setWidgetResizable(True)

                scroll_content = QWidget()
                scroll_content.setStyleSheet("background-color: #151A21;")
                scroll_area.setWidget(scroll_content)

                layout = QVBoxLayout(scroll_content)
                layout.addWidget(content_label)

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

                content_label.setFont(self.predator_font)
                content_label.setStyleSheet(
                    f"color: #00B0C8; font-size: 18px; background-color: #151A21; padding: 10px;"
                    f"font-family: '{self.predator_font.family()}';"
                )
                content_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
                self.internal_window.layout().addWidget(scroll_area)

            except Exception as e:
                # Log the error and display a message
                print(f"Error loading category content: {e}")
                error_label = QLabel("Error: Unable to load content.")
                error_label.setStyleSheet("color: red; font-size: 18px;")
                self.internal_window.layout().addWidget(error_label)

        # Start by showing the buttons
        showButtons()
        self.internal_window.updateContent(text)
