#####################################
#                                   #
#  @author      : 00xWolf           #
#    GitHub    : @mmsaeed509       #
#    Developer : Mahmoud Mohamed   #
#  﫥  Copyright : Exodia OS         #
#                                   #
#####################################

import os
import yaml
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QScrollArea, QFrame, QLineEdit
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QBrush, QColor, QPen, QPolygon, QRegion
from Xlib import display
from Xlib.Xatom import STRING


# Function to set WM_CLASS for the window
def set_wm_class(win_id, instance_name, class_name):
    # Set the WM_CLASS property for a window.
    disp = display.Display()
    window = disp.create_resource_object('window', win_id)
    wm_class_atom = disp.intern_atom('WM_CLASS')
    value = f'{instance_name}\0{class_name}\0'.encode('utf-8')
    window.change_property(wm_class_atom, STRING, 8, value)
    disp.flush()


def get_available_roles():

    roles_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "profiles")
    if os.path.exists(roles_dir) and os.path.isdir(roles_dir):
        return [d for d in os.listdir(roles_dir) if os.path.isdir(os.path.join(roles_dir, d))]
    return []

import os
import yaml

def save_role_to_yaml(role_name):
    config_dir = os.path.expanduser("~/.config/exodia-assistant")
    os.makedirs(config_dir, exist_ok=True)  # Ensure directory exists
    yaml_path = os.path.join(config_dir, "role.yaml")

    data = {"selected_role": role_name}

    with open(yaml_path, 'w') as yaml_file:
        yaml.dump(data, yaml_file, default_flow_style=False)

def load_role_from_yaml():
    yaml_path = os.path.expanduser("~/.config/exodia-assistant/role.yaml")

    if os.path.exists(yaml_path):
        try:
            with open(yaml_path, 'r') as yaml_file:
                data = yaml.safe_load(yaml_file)
                return data.get("selected_role")
        except Exception:
            return None
    return None

class RoleSelectionWindow(QWidget):
    def __init__(self, parent=None, predator_font=None):
        super().__init__(parent)
        self.layout = None
        self.current_role = None
        self.available_roles = None
        self.filtered_roles = None
        self.predator_font = predator_font
        self.selected_role = None
        self.roles_container = None
        self.scroll_area = None
        self.search_text = ""
        self.initUI()

    def initUI(self):
        # Set window properties
        self.setFixedSize(900, 700)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setMask(self.create_role_selection_mask())
        # Set WM_CLASS after the window is shown
        self.set_wm_class()
        print("UI Initialized")

        # Main layout
        self.layout = QVBoxLayout(self)
        # self.layout.setContentsMargins(x, y, width, height)
        self.layout.setContentsMargins(220, 120, 220, 120)
        self.layout.setSpacing(10)  # Add some spacing between elements

        # Title
        title_label = QLabel("Select a Role", self)
        title_label.setAlignment(Qt.AlignCenter)
        if self.predator_font:
            title_label.setFont(self.predator_font)
            title_label.setStyleSheet(f"color: #00B0C8; font-size: 24px; font-family: '{self.predator_font.family()}';")
        else:
            title_label.setStyleSheet("color: #00B0C8; font-size: 24px;")
        self.layout.addWidget(title_label)

        # Search bar
        search_layout = QHBoxLayout()
        search_layout.setContentsMargins(0, 10, 0, 10)

        # Search text field
        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText("Search roles...")
        self.search_field.setFixedHeight(40)
        if self.predator_font:
            self.search_field.setFont(self.predator_font)
            self.search_field.setStyleSheet(f"""
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
        else:
            self.search_field.setStyleSheet("""
                QLineEdit {
                    background-color: #151A21;
                    color: white;
                    border: 1px solid #00B0C8;
                    border-radius: 5px;
                    padding: 5px;
                }
                QLineEdit:focus {
                    border: 2px solid #00B0C8;
                }
            """)
        self.search_field.textChanged.connect(self.search_roles)

        # Search button
        search_button = QPushButton("Search", self)
        search_button.setFixedSize(100, 40)
        search_button.setCursor(Qt.PointingHandCursor)
        if self.predator_font:
            search_button.setFont(self.predator_font)
            search_button.setStyleSheet(f"""
                QPushButton {{
                    background-color: #00B0C8;
                    color: white;
                    border-radius: 5px;
                    font-family: '{self.predator_font.family()}';
                }}
                QPushButton:hover {{
                    background-color: #0086A8;
                }}
                QPushButton:pressed {{
                    background-color: #005F78;
                }}
            """)
        else:
            search_button.setStyleSheet("""
                QPushButton {
                    background-color: #00B0C8;
                    color: white;
                    border-radius: 5px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #0086A8;
                }
                QPushButton:pressed {
                    background-color: #005F78;
                }
            """)
        search_button.clicked.connect(lambda: self.search_roles(self.search_field.text()))

        search_layout.addWidget(self.search_field)
        search_layout.addWidget(search_button)

        self.layout.addLayout(search_layout)

        # Scroll area for roles
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setStyleSheet("""
            QScrollArea { 
                border: none; 
                background-color: transparent;
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
                background: none;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)

        # Create and populate the role container
        self.create_roles_container()

        self.layout.addWidget(self.scroll_area)

        # Buttons layout
        buttons_layout = QHBoxLayout()
        buttons_layout.setContentsMargins(0, 10, 0, 0)  # Add some top margin
        buttons_layout.setSpacing(20)  # Add spacing between buttons
        buttons_layout.setAlignment(Qt.AlignCenter)  # Center the buttons

        # OK button
        ok_button = QPushButton("OK", self)
        ok_button.setFixedSize(100, 40)
        ok_button.setCursor(Qt.PointingHandCursor)  # Change cursor to hand when hovering
        if self.predator_font:
            ok_button.setFont(self.predator_font)
            ok_button.setStyleSheet(f"""
                QPushButton {{
                    background-color: #00B0C8;
                    color: white;
                    border-radius: 5px;
                    font-family: '{self.predator_font.family()}';
                }}
                QPushButton:hover {{
                    background-color: #0086A8;
                }}
                QPushButton:pressed {{
                    background-color: #005F78;
                }}
            """)
        else:
            ok_button.setStyleSheet("""
                QPushButton {
                    background-color: #00B0C8;
                    color: white;
                    border-radius: 5px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #0086A8;
                }
                QPushButton:pressed {
                    background-color: #005F78;
                }
            """)
        ok_button.clicked.connect(self.save_and_close)

        # Cancel button
        cancel_button = QPushButton("CANCEL", self)
        cancel_button.setFixedSize(100, 40)
        cancel_button.setCursor(Qt.PointingHandCursor)  # Change cursor to hand when hovering
        if self.predator_font:
            cancel_button.setFont(self.predator_font)
            cancel_button.setStyleSheet(f"""
                QPushButton {{
                    background-color: #151A21;
                    color: white;
                    border-radius: 5px;
                    font-family: '{self.predator_font.family()}';
                }}
                QPushButton:hover {{
                    background-color: #1A2530;
                }}
                QPushButton:pressed {{
                    background-color: #0F1218;
                }}
            """)
        else:
            cancel_button.setStyleSheet("""
                QPushButton {
                    background-color: #151A21;
                    color: white;
                    border-radius: 5px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #1A2530;
                }
                QPushButton:pressed {
                    background-color: #0F1218;
                }
            """)
        cancel_button.clicked.connect(self.close)

        buttons_layout.addWidget(ok_button)
        buttons_layout.addWidget(cancel_button)

        self.layout.addLayout(buttons_layout)

    # Set the WM_CLASS property with instance and class names
    def set_wm_class(self):
        # Get the native window ID
        win_id = self.winId().__int__()
        set_wm_class(win_id, "exodiaos-assistant", "ExodiaOS Assistant")

    @staticmethod
    def create_role_selection_mask():

        points = [
            QPoint(850, 0),  # Top right corner, 1
            QPoint(900, 50),  # Right top-middle, a bit down, 2
            QPoint(900, 700),  # Bottom right corner, 3
            QPoint(50, 700),  # Bottom left-middle, 4
            QPoint(0, 650),  # Bottom left corner, 5
            QPoint(0, 0)  # Top left corner, 6
        ]
        polygon = QPolygon(points)
        return QRegion(polygon)

    def search_roles(self, text):
        """
        Filter roles based on search text.

        Args:
            text (str): The search text
        """
        self.search_text = text.lower()
        self.create_roles_container()

    def create_roles_container(self):
        """
        Create and populate the container with available roles.
        This method can be called to refresh the Roles list.
        """
        # Container for roles
        self.roles_container = QWidget()
        self.roles_container.setStyleSheet("background-color: transparent;")
        roles_layout = QVBoxLayout(self.roles_container)
        roles_layout.setAlignment(Qt.AlignTop)  # Align content to the top

        # Add role buttons
        self.available_roles = get_available_roles()
        self.current_role = load_role_from_yaml()

        # Filter roles based on search text
        if self.search_text:
            self.filtered_roles = [role for role in self.available_roles if self.search_text in role.lower()]
        else:
            self.filtered_roles = self.available_roles

        # Set spacing for the role layout
        roles_layout.setSpacing(10)

        for role in self.filtered_roles:
            role_frame = QFrame()
            role_frame.setCursor(Qt.PointingHandCursor)  # Change cursor to hand when hovering
            role_frame.setStyleSheet("""
                QFrame {
                    background-color: #151A21;
                    border-radius: 5px;
                    margin: 5px;
                }
                QFrame:hover {
                    background-color: #1A2530;
                }
            """)

            # Make the frame clickable
            role_frame.mousePressEvent = lambda event, r=role: self.select_role(r)

            role_layout = QHBoxLayout(role_frame)

            role_label = QLabel(role)
            if self.predator_font:
                role_label.setFont(self.predator_font)
                role_label.setStyleSheet(f"color: #00B0C8; font-size: 18px; font-family: '{self.predator_font.family()}';")
            else:
                role_label.setStyleSheet("color: #00B0C8; font-size: 18px;")

            role_layout.addWidget(role_label)

            # Add a status indicator instead of a button
            status_label = QLabel("Select")
            status_label.setFixedSize(100, 40)
            status_label.setAlignment(Qt.AlignCenter)
            if self.predator_font:
                status_label.setFont(self.predator_font)
                status_label.setStyleSheet(f"""
                    QLabel {{
                        background-color: #00B0C8;
                        color: white;
                        border-radius: 5px;
                        padding: 5px;
                        font-family: '{self.predator_font.family()}';
                    }}
                """)
            else:
                status_label.setStyleSheet("""
                    QLabel {
                        background-color: #00B0C8;
                        color: white;
                        border-radius: 5px;
                        padding: 5px;
                    }
                """)

            # If this is the current role, mark it as selected
            if role == self.current_role:
                self.selected_role = role
                role_frame.setStyleSheet("""
                    QFrame {
                        background-color: #1A2530;
                        border: 2px solid #00B0C8;
                        border-radius: 5px;
                        margin: 5px;
                    }
                    QFrame:hover {
                        background-color: #1A2530;
                    }
                """)
                status_label.setText("Selected")

            role_layout.addWidget(status_label)

            # Store the status label for later reference
            role_frame.status_label = status_label

            roles_layout.addWidget(role_frame)

        self.scroll_area.setWidget(self.roles_container)

    def select_role(self, role_name):
        """
        Select a role.

        Args:
            role_name (str): The name of the role to select
        """
        self.selected_role = role_name

        # Update the UI to show the selected role
        for i in range(self.layout.count()):
            widget = self.layout.itemAt(i).widget()
            if isinstance(widget, QScrollArea):
                scroll_content = widget.widget()
                for j in range(scroll_content.layout().count()):
                    frame = scroll_content.layout().itemAt(j).widget()
                    if isinstance(frame, QFrame):
                        role_layout = frame.layout()
                        if role_layout.count() > 0:
                            label_item = role_layout.itemAt(0)
                            if label_item and isinstance(label_item.widget(), QLabel):
                                label = label_item.widget()
                                if label.text() == role_name:
                                    # Selected role
                                    frame.setStyleSheet("""
                                        QFrame {
                                            background-color: #1A2530;
                                            border: 2px solid #00B0C8;
                                            border-radius: 5px;
                                            margin: 5px;
                                        }
                                        QFrame:hover {
                                            background-color: #1A2530;
                                        }
                                    """)
                                    if hasattr(frame, 'status_label'):
                                        frame.status_label.setText("Selected")
                                else:
                                    # Non-selected role
                                    frame.setStyleSheet("""
                                        QFrame {
                                            background-color: #151A21;
                                            border-radius: 5px;
                                            margin: 5px;
                                        }
                                        QFrame:hover {
                                            background-color: #1A2530;
                                        }
                                    """)
                                    if hasattr(frame, 'status_label'):
                                        frame.status_label.setText("Select")

    def save_and_close(self):
        """
        Save the selected role and close the window.
        """
        if self.selected_role:
            save_role_to_yaml(self.selected_role)
        self.close()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw background
        painter.setBrush(QBrush(QColor("#0E1218")))
        painter.drawRect(self.rect())

        border_points = [
            QPoint(850, 0),  # Top right corner, 1
            QPoint(900, 50),  # Right top-middle, a bit down, 2
            QPoint(900, 700),  # Bottom right corner, 3
            QPoint(50, 700),  # Bottom left-middle, 4
            QPoint(0, 650),  # Bottom left corner, 5
            QPoint(0, 0)  # Top left corner, 6
        ]
        border_polygon = QPolygon(border_points)

        border_pen = QPen(QColor("#00B0C8"))
        border_pen.setWidth(10)  # Increased border width
        painter.setPen(border_pen)
        painter.drawPolygon(border_polygon)

        # Draw title text if predator_font is available
        if hasattr(self, 'predator_font') and self.predator_font:
            painter.setFont(self.predator_font)
            painter.setPen(QColor("#00B0C8"))
