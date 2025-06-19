from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QScrollArea, QLineEdit, QFrame
from ...utils import ui_utils, font_utils, file_utils, ui_utils, html_utils

def displayKeybindingContent(internal_window, predator_font):
    text = ""
    # Base directory for HTML files
    html_dir = "../../assets/html/Keybinding"

    def clearLayout():
        """Clears the layout of the internal window."""
        while internal_window.layout().count():
            item = internal_window.layout().takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def createCustomButton(label, html_file):
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
                background-color: #0086A8;
            }}
            QPushButton:pressed {{
                background-color: #005F78;
            }}
            """
        )

        text_label = QLabel(label)
        text_label.setAlignment(Qt.AlignCenter)
        text_label.setWordWrap(True)
        text_label.setStyleSheet(
            f"color: white; font-family: '{predator_font.family()}'; font-size: 18px;"
        )

        layout = QVBoxLayout()
        layout.addWidget(text_label)
        layout.setContentsMargins(0, 0, 0, 0)
        button.setLayout(layout)

        button.clicked.connect(lambda _, file=html_file: showHTML(file))
        return button

    def showButtons(keyword=None):
        """Displays the main tip buttons filtered by keyword."""
        clearLayout()

        # Define button labels and corresponding HTML file names
        Keybinding_data = [
            ("BSPWM", "BSPWM.html"),
            ("DWM", "DWM.html"),
            ("I3WM", "I3WM.html")
        ]

        # Create a scrollable widget
        scroll_widget = QWidget()
        scroll_widget.setStyleSheet("background: transparent;")  # Make the scroll widget transparent
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins for a cleaner look

        # Add buttons to the scrollable widget
        row_layout = None
        for index, (label, html_file) in enumerate(Keybinding_data):
            if index % 3 == 0:
                row_layout = QHBoxLayout()
                row_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins for a cleaner look
                scroll_layout.addLayout(row_layout)

            button = createCustomButton(label, html_file)
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
        internal_window.layout().addWidget(scroll_area)

    def showHTML(html_file):
        """Displays the content of the selected HTML file."""
        try:
            # Clear the existing layout
            clearLayout()

            # Create a "Back" button to return to the buttons view
            back_button = QPushButton("Back")
            back_button.setFont(predator_font)
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
                    background-color: #00343C;
                }
                """
            )
            back_button.clicked.connect(showButtons)

            # Add the "Back" button to the top layout
            top_layout = QHBoxLayout()
            top_layout.addWidget(back_button, alignment=Qt.AlignLeft)

            top_widget = QWidget()
            top_widget.setLayout(top_layout)
            internal_window.layout().addWidget(top_widget)

            # Load the HTML content
            html_content = html_utils.loadHTMLContent(html_dir, html_file, predator_font.family())

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
            scroll_content.setStyleSheet("background-color: #006c7a;")
            scroll_area.setWidget(scroll_content)

            layout = QVBoxLayout(scroll_content)
            layout.addWidget(content_label)

            scroll_area.setStyleSheet("""
                QScrollArea { 
                    border: none;
                    padding: 0;
                    background-color: #1E1E1E;
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

            content_label.setFont(predator_font)
            content_label.setStyleSheet(
                f"color: #00B0C8; font-size: 18px; background-color: #151A21; padding: 10px;"
                f"font-family: '{predator_font.family()}';"
            )
            content_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
            internal_window.layout().addWidget(scroll_area)

        except Exception as e:
            # Log the error and display a message
            print(f"Error loading HTML content: {e}")
            error_label = QLabel("Error: Unable to load content.")
            error_label.setStyleSheet("color: red; font-size: 18px;")
            internal_window.layout().addWidget(error_label)

    showButtons()
    internal_window.updateContent(text)
    
    return internal_window