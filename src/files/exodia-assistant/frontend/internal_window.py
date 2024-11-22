#####################################
#                                   #
#  @author      : 00xWolf           #
#    GitHub    : @mmsaeed509       #
#    Developer : Mahmoud Mohamed   #
#  﫥  Copyright : Exodia OS         #
#                                   #
#####################################
import os

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QColor, QBrush, QRegion, QPolygon, QPen, QFontDatabase, QFont
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QScrollArea

class InternalWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Set the geometry (position and size) of the internal window
        # self.setGeometry(x, y, width, height)
        self.predator_font = None
        self.setGeometry(300, 100, 1140, 640)
        self.setAttribute(Qt.WA_TranslucentBackground)  # Make the background transparent
        self.polygon = self.createCustomMask()  # Store the polygon used for the mask
        self.content_label = QLabel(self)
        self.content_label.setGeometry(self.rect())
        self.content_label.setStyleSheet("color: white; font-size: 20px; padding: 0px;")

        # Load and apply Predator font
        self.loadPredatorFont()

        # Create the scroll area
        scroll_area = QScrollArea(self)
        scroll_area.setGeometry(10, 20, 1100, 600)  # Set scroll area size within the internal window
        # scroll_area.setGeometry(self.rect())  # Set the scroll area to the full size of the window
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setWidgetResizable(True)  # Ensure the content resizes with the window

        # Create a widget to hold the content (which will be scrollable)
        scroll_content = QWidget()
        scroll_content.setStyleSheet("background-color: #0E1218;")  # Transparent background for content
        scroll_area.setWidget(scroll_content)

        # Create a layout for the scrollable content
        layout = QVBoxLayout(scroll_content)

        # Content label that will be scrollable
        self.content_label = QLabel(scroll_content)
        self.content_label.setStyleSheet("color: #0E1218; font-size: 20px; padding: 0px;")
        self.content_label.setWordWrap(True)  # Allow the text to wrap

        layout.addWidget(self.content_label)  # Add the label to the layout

        # Remove border and customize scroll bar colors
        scroll_area.setStyleSheet("""
            QScrollArea { border: none; }
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
        self.content_label.setFont(self.predator_font)  # Apply Predator font
        self.content_label.setStyleSheet(
            f"color: #00B0C8; font-size: 18px; background-color: #0E1218; padding: 10px;"
            f"font-family: '{self.predator_font.family()}';"
        )
        self.content_label.setTextInteractionFlags(Qt.TextSelectableByMouse)

    def loadPredatorFont(self):

        # Load the font from the Fonts directory
        font_path = os.path.join(os.path.dirname(__file__), '../Fonts', 'Squares-Bold.otf')
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id == -1:
            print("Failed to load predator font.")
        else:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            self.predator_font = QFont(font_family, 30, QFont.Bold)

    def createCustomMask(self):
        # Define points for an 8-sided polygon
        points = [
            QPoint(1110, 0),   # Top center, 1
            QPoint(1140, 30),  # Top right, 2
            QPoint(1140, 640), # Middle right, 3
            QPoint(0, 640),   # Bottom center, 4
            # QPoint(30, 640),   # Bottom center, 4
            # QPoint(0, 610),    # Bottom left, 5
            QPoint(0, 0)     # Middle left, 6
        ]

        polygon = QPolygon(points)
        mask = QRegion(polygon)
        self.setMask(mask)  # Apply the mask to make the window non-rectangular
        return polygon  # Return the polygon for use in the paint event

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw the custom shape with a color fill
        painter.setBrush(QBrush(QColor("#0E1218")))  # Use a custom background color
        painter.drawPolygon(self.polygon)  # Draw the filled polygon

        # Draw the border with the specified color
        pen = QPen(QColor("#00B0C8"), 5)  # Create a pen with the desired color and border width
        painter.setPen(pen)
        painter.drawPolygon(self.polygon)  # Draw the polygon border

    def updateContent(self, text):
        # Assuming you have a QLabel or QTextEdit in the window to display content
        self.content_label.setText(text)  # Update the label with the provided text
