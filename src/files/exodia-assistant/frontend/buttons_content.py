#####################################
#                                   #
#  @author      : 00xWolf           #
#    GitHub    : @mmsaeed509       #
#    Developer : Mahmoud Mohamed   #
#  﫥  Copyright : Exodia OS         #
#                                   #
#####################################

from PyQt5.QtGui import QFontDatabase, QFont, QIcon
import os
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPolygon, QRegion
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QScrollArea


def createCustomButtonMask():
    """Creates a custom QRegion mask for buttons."""
    button_points = [
        QPoint(200, 0),  # Top right
        QPoint(240, 30),  # Bottom right
        QPoint(240, 100),  # Bottom right curve
        QPoint(30, 100),  # Bottom left curve
        QPoint(0, 70),  # Bottom left
        QPoint(0, 0),  # Top left
    ]
    polygon = QPolygon(button_points)
    return QRegion(polygon)


def setupButton(button, font_family):
    """Applies custom styles and mask to the button."""
    button.setMask(createCustomButtonMask())
    button.setStyleSheet(f"""
        QPushButton {{
            font-family: {font_family};
            background-color: #00B0C8;
            color: black;
            font-size: 18px;
            font-weight: bold;
            padding: 5px;
            border: none;
        }}
    """)

def loadPredatorFont():
    # Load the font from the Fonts directory
    font_path = os.path.join(os.path.dirname(__file__), '../Fonts', 'Squares-Bold.otf')
    font_id = QFontDatabase.addApplicationFont(font_path)
    if font_id == -1:
        print("Failed to load predator font.")
        return None
    else:
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        return QFont(font_family, 30, QFont.Bold)

def loadHTMLContent(directory, filename, font_family):
    """
    Loads and formats HTML content from a specified file.

    Args:
        directory (str): The directory containing the HTML file.
        filename (str): The name of the HTML file.
        font_family (str): The font family to apply to the content.

    Returns:
        str: The formatted HTML content.
    """
    # Define the path to the HTML file
    html_file_path = os.path.join(os.path.dirname(__file__), directory, filename)

    try:
        # Read the content of the HTML file
        with open(html_file_path, "r", encoding="utf-8") as html_file:
            html_content = html_file.read()
    except FileNotFoundError:
        html_content = """
        <div style="color: red; text-align: center; font-size: 18px; padding: 20px;">
            Error: Could not find the content file at <code>{}</code>.
        </div>
        """.format(html_file_path)
    except Exception as e:
        html_content = """
        <div style="color: red; text-align: center; font-size: 18px; padding: 20px;">
            Error: An unexpected error occurred while reading the content file.<br>
            Details: {}
        </div>
        """.format(str(e))

    # Add a placeholder for the font family if it's not already formatted
    if "{}" in html_content:
        return html_content.format(font_family)
    else:
        return f"<div style='font-family: {font_family};'>{html_content}</div>"

class ButtonContent:

    def __init__(self, internal_window):
        self.internal_window = internal_window
        self.predator_font = loadPredatorFont()

    def clearButtons(self):
        # Remove all button widgets from the internal window
        for i in reversed(range(self.internal_window.layout().count())):
            widget = self.internal_window.layout().itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

    def displayWelcomeContent(self):
        # Clear previous buttons
        if not self.internal_window.layout():
            self.internal_window.setLayout(QVBoxLayout())
            self.clearButtons()
        else:
            self.clearButtons()

        # Load and format the HTML content
        text = loadHTMLContent('./HTML-files', 'displayWelcomeContent.html', self.predator_font.family())

        # Update the content of the internal window
        self.internal_window.updateContent(text)


    def displayKeybindingContent(self):

        self.clearButtons() # Clear previous buttons
        # Load and format the HTML content
        text = loadHTMLContent('./HTML-files', 'displayKeybindingContent.html', self.predator_font.family())
        # Update the content of the internal window
        self.internal_window.updateContent(text)

    def displaySettingContent(self):

        self.clearButtons() # Clear previous buttons
        # Load and format the HTML content
        text = loadHTMLContent('./HTML-files', 'displaySettingContent.html', self.predator_font.family())
        # Update the content of the internal window
        self.internal_window.updateContent(text)


    def displayDevelopersContent(self):

        self.clearButtons() # Clear previous buttons
        # Load and format the HTML content
        text = loadHTMLContent('./HTML-files', 'displayDevelopersContent.html', self.predator_font.family())
        # Update the content of the internal window
        self.internal_window.updateContent(text)

    def displayTipsContent(self):

        text = ""
        # Base directory for HTML files
        html_dir = "./HTML-files/tips"

        def clearLayout():
            """Clears the layout of the internal window."""
            while self.internal_window.layout().count():
                item = self.internal_window.layout().takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()

        def createCustomButton(label, html_file):
            """Creates a custom button widget with word-wrapped text and a custom shape."""
            # Create a QPushButton and apply the custom mask
            button = QPushButton()
            button.setFixedSize(240, 100)
            button.setMask(createCustomButtonMask())
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

            # Label for text inside the button
            text_label = QLabel(label)
            text_label.setAlignment(Qt.AlignCenter)
            text_label.setWordWrap(True)
            text_label.setStyleSheet(
                f"color: white; font-family: '{self.predator_font.family()}'; font-size: 18px;"
            )

            # Layout to combine QLabel inside QPushButton
            layout = QVBoxLayout()
            layout.addWidget(text_label)
            layout.setContentsMargins(0, 0, 0, 0)  # Remove padding
            button.setLayout(layout)

            # Connect button click to showHTML
            button.clicked.connect(lambda _, file=html_file: showHTML(file))
            return button

        def showButtons():
            """Displays the main tip buttons grouped into rows."""
            clearLayout()

            # Define button labels and corresponding HTML file names
            tips_data = [
                ("PGP signature Error", "PGP-signature-Error.html"),
                ("Adding Music", "Adding-Music.html"),
                ("Set Keyboard Layout", "Set-Keyboard-Layout.html"),
                ("Changing SDDM User Picture", "Changing-SDDM-User-Picture.html"),
                ("Create Your Own Theme", "Create-Your-Own-Theme.html"),
                ("Setup Custom Monitors Config", "Setup-Custom-Monitors-Config.html"),
                ("Setup Polybar Modules", "Setup-Polybar-Modules.html"),
            ]

            # Create a layout to organize buttons
            layout = QVBoxLayout()
            row_layout = None

            # Add buttons dynamically
            for index, (label, html_file) in enumerate(tips_data):
                # Create a new row layout every 3 buttons
                if index % 3 == 0:
                    row_layout = QHBoxLayout()
                    layout.addLayout(row_layout)

                # Create the custom button and add it to the row
                button = createCustomButton(label, html_file)
                row_layout.addWidget(button)

            # Add the main layout to the internal window
            widget = QWidget()
            widget.setLayout(layout)
            self.internal_window.layout().addWidget(widget)

        def showHTML(html_file):
            """Displays the HTML content of a specific tip with scrolling and text copy support."""
            clearLayout()

            # Create a back button
            back_button = QPushButton("Back")
            setupButton(back_button, self.predator_font.family())
            back_button.setFixedSize(100, 40)
            back_button.clicked.connect(showButtons)

            # Add the back button to the layout
            top_layout = QHBoxLayout()
            top_layout.addWidget(back_button, alignment=Qt.AlignLeft)

            # Create a widget for the back button
            top_widget = QWidget()
            top_widget.setLayout(top_layout)
            self.internal_window.layout().addWidget(top_widget)

            # Render the HTML content using the provided loadHTMLContent function
            html_content = loadHTMLContent(html_dir, html_file, self.predator_font.family())

            # Create a QLabel to display the content
            content_label = QLabel()
            content_label.setTextFormat(Qt.RichText)
            content_label.setWordWrap(True)
            content_label.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
            content_label.setText(html_content)

            # Create the scroll area, with `self.internal_window` as the parent
            scroll_area = QScrollArea()  # Use internal_window as the parent widget
            # --------- setGeometry(x, y, width, height)
            scroll_area.setGeometry(40, 20, 1100, 600)  # Set scroll area size within the internal window
            scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            scroll_area.setWidgetResizable(True)  # Ensure the content resizes with the window

            # Create a widget to hold the content (which will be scrollable)
            scroll_content = QWidget()
            scroll_content.setStyleSheet("background-color: #00B0C8; border-size: 2px;")  # Transparent background and no border
            scroll_area.setWidget(scroll_content)

            # Create a layout for the scrollable content
            layout = QVBoxLayout(scroll_content)

            # Add the content label to the layout
            layout.addWidget(content_label)

            # Remove border and customize scroll bar colors
            scroll_area.setStyleSheet("""
                QScrollArea { 
                    border: none;  /* Removes border around the QScrollArea */
                    padding: 0;     /* Removes any padding inside the QScrollArea */
                    background-color: #1E1E1E;  /* Set background color to dark gray */
                }
                QScrollBar:vertical {
                    background: #222;  /* Background color of the vertical scrollbar */
                    width: 10px;       /* Width of the scrollbar */
                    margin: 0 0 0 0;   /* Margin around the scrollbar */
                }
                QScrollBar::handle:vertical {
                    background: #00B0C8;  /* Color of the scrollbar handle */
                    border-radius: 5px;    /* Rounded corners for the scrollbar handle */
                }
                QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                    background: none;      /* Hide the add and subtract buttons */
                }
                QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                    background: none;      /* Hide the add and subtract page areas */
                }
            """)

            # Create QLabel for the content, To be selectable and copyable
            content_label.setFont(self.predator_font)  # Apply Predator font
            content_label.setStyleSheet(
                f"color: #00B0C8; font-size: 18px; background-color: #0E1218; padding: 10px;"
                f"font-family: '{self.predator_font.family()}';"
            )
            content_label.setTextInteractionFlags(Qt.TextSelectableByMouse)

            # Add the scroll area to the layout
            self.internal_window.layout().addWidget(scroll_area)

        # Initialize the tips view with buttons
        showButtons()
        self.internal_window.updateContent(text)
