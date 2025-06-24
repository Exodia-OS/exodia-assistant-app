#####################################
#                                   #
#  @author      : 00xWolf           #
#    GitHub    : @mmsaeed509       #
#    Developer : Mahmoud Mohamed   #
#  﫥  Copyright : Exodia OS         #
#                                   #
#####################################

import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QPushButton, QLabel, QHBoxLayout, QTabWidget
from PyQt5.QtCore import Qt
from ...core import role as role_logic
from ...utils import font_utils, roles_utils

class RoleTabUI(QWidget):
    """
    UI class for displaying and managing roles in Exodia Assistant.
    Uses logic from role.py and roles_utils.py.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(0, 0, 800, 600)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.predator_font = font_utils.loadPredatorFont()
        if self.predator_font:
            self.predator_font.setPointSize(12)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("background-color: transparent; border: none;")
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.scroll_area.setWidget(self.content_widget)
        self.layout.addWidget(self.scroll_area)
        self.internal_window = None
        self.show_role_overview()

    def show_role_overview(self):
        """Display the main role overview or selection UI."""
        self.clear_content()
        overview_html = role_logic.get_role_overview_html(self.predator_font)
        label = QLabel()
        label.setTextFormat(Qt.RichText)
        label.setWordWrap(True)
        label.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        label.setText(overview_html)
        label.setFont(self.predator_font)
        label.setStyleSheet(f"color: #00B0C8; font-size: 18px; background-color: #151A21; padding: 10px; font-family: '{self.predator_font.family()}';")
        self.content_layout.addWidget(label)

    def show_role_content(self, role_name):
        """Display the content for a specific role."""
        self.clear_content()
        html = role_logic.get_role_content_html(role_name, self.predator_font)
        label = QLabel()
        label.setTextFormat(Qt.RichText)
        label.setWordWrap(True)
        label.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        label.setText(html)
        label.setFont(self.predator_font)
        label.setStyleSheet(f"color: #00B0C8; font-size: 18px; background-color: #151A21; padding: 10px; font-family: '{self.predator_font.family()}';")
        self.content_layout.addWidget(label)

    def clear_content(self):
        """Remove all widgets from the content layout."""
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater() 