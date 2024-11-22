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
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel


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

    def displayTipsContent(self):
        text = """"""

        # Check if internal_window already has a layout
        if not self.internal_window.layout():
            self.internal_window.setLayout(QVBoxLayout())

            # Create button containers
            button_container_1 = QWidget()
            button_layout_1 = QHBoxLayout(button_container_1)

            button_container_2 = QWidget()
            button_layout_2 = QHBoxLayout(button_container_2)

            button_container_3 = QWidget()
            button_layout_3 = QHBoxLayout(button_container_3)

            # Define button labels for each row
            first_row_labels = [
                "PGP signature Error",
                "Adding Music",
                "Set Keyboard Layout"
            ]

            second_row_labels = [
                "Changing SDDM User Picture",
                "Create Your Own Theme",
                "Setup Custom Monitors Config",
            ]

            third_row_labels = [
                "Setup Polybar Modules",
            ]

            # Function to create buttons
            def createButton(label, layout):
                button = QPushButton()
                setupButton(button, self.predator_font.family())
                button.setFixedSize(240, 100)  # Custom size for shaped buttons

                # Create a QLabel for the text inside the button
                label_widget = QLabel(label)
                label_widget.setWordWrap(True)  # Enable word wrapping
                label_widget.setAlignment(Qt.AlignCenter)  # Center-align the text

                # Set font to Predator font and increase font size
                font = label_widget.font()
                font.setFamily(self.predator_font.family())  # Set Predator font family
                font.setPointSize(14)  # Increase font size (adjust as needed)
                label_widget.setFont(font)

                # Set the QLabel as the button's content
                button.setLayout(QVBoxLayout())
                button.layout().addWidget(label_widget)

                button.clicked.connect(lambda _, cmd=label: self.runCommand(cmd))
                layout.addWidget(button)

            # Create first row of buttons with a custom shape
            for label in first_row_labels:
                createButton(label, button_layout_1)

            # Create second row of buttons with a custom shape
            for label in second_row_labels:
                createButton(label, button_layout_2)

            # Create third row of buttons with a custom shape
            for label in third_row_labels:
                createButton(label, button_layout_3)

            # Add the button containers to the internal window's layout
            self.internal_window.layout().addWidget(button_container_1)
            self.internal_window.layout().addWidget(button_container_2)
            self.internal_window.layout().addWidget(button_container_3)

        else:
            print("Internal window already has a layout.")

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
