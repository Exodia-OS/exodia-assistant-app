import os
import shutil
import getpass
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QBrush, QColor, QFont, QFontDatabase, QPen, QPolygon, QRegion
from PyQt5.QtWidgets import QMainWindow, QPushButton, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QCheckBox, QComboBox, QSlider, QScrollArea, QFrame, QFileDialog, QMessageBox
import utils


def createButtonMask():
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


def createCloseButtonMask():
    button_points = [
        QPoint(200, 0),  # Top right
        QPoint(240, 50),  # Bottom right
        QPoint(200, 100),  # Bottom right curve
        QPoint(40, 100),  # Bottom left curve
        QPoint(0, 50),  # Bottom left
        QPoint(40, 0),  # Top left
    ]
    polygon = QPolygon(button_points)
    return QRegion(polygon)


class SettingWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.toggle_button = None
        self.close_button = None
        self.is_auto_start = None
        self.custom_font = None
        self.config_path = os.path.expanduser('~/.config/bspwm/exodia.conf')  # Path to the config file
        self.theme = "dark"  # Default theme
        self.font_size = 18  # Default font size
        self.news_refresh_rate = 60  # Default refresh rate in minutes
        self.tab_widget = None
        self.initUI()

    def initUI(self):
        # self.setGeometry(x, y, width, height)
        self.setGeometry(300, 100, 1140, 640)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.setMask(self.createMask())
        self.loadCustomFont()
        # Apply the predator font to the entire window
        if self.custom_font:
            self.setFont(self.custom_font)
        self.loadAutoStartStatus()  # Load the current auto-start status
        self.addCloseButton()  # Add the close button
        self.setupTabs()  # Set up the tabs
        print("UI Initialized")

    @staticmethod
    def createMask():
        points = [
            QPoint(910, 100),  # Top center, 1
            QPoint(940, 130),  # Top right, 2
            QPoint(940, 440),  # Middle right, 3
            QPoint(230, 440),  # Bottom center, 4
            QPoint(200, 410),  # Bottom left, 5
            QPoint(200, 100),  # Middle left, 6
        ]
        polygon = QPolygon(points)
        return QRegion(polygon)

    def loadCustomFont(self):
        self.custom_font = utils.loadPredatorFont()
        if self.custom_font:
            self.custom_font.setPointSize(20)

    def loadAutoStartStatus(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as config_file:
                for line in config_file:
                    if 'exodia-assistant-auto-start' in line:
                        self.is_auto_start = line.split('=')[1].strip().lower() == 'true'
                        break
        else:
            self.is_auto_start = False  # Default to false if the file does not exist
        print(f"Auto-start status loaded: {self.is_auto_start}")

    def addCloseButton(self):

        self.close_button = QPushButton('X', self)
        #            self.setGeometry(x, y, width, height)
        self.close_button.setGeometry(889, 115, 30, 30)  # Positioned above the toggle button
        # Get the font family name for use in StyleSheet
        font_family = self.custom_font.family() if self.custom_font else "Squares-Bold"
        self.close_button.setStyleSheet(f"""
            QPushButton {{
                background-color: #151A21;
                color: #00B0C8;
                font-family: '{font_family}';
                font-size: 30px;
                font-weight: bold;
                border-radius: 0px;
            }}
        """)
        # # Use the same mask for custom shape
        # self.close_button.setMask(createCloseButtonMask())
        self.close_button.clicked.connect(self.close)

    def setupTabs(self):
        # Create a central widget to hold the tab widget
        central_widget = QWidget(self)
        central_widget.setGeometry(220, 130, 700, 250)
        central_widget.setStyleSheet("background-color: transparent;")

        # Create a layout for the central widget
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)

        # Create the tab widget
        self.tab_widget = QTabWidget(central_widget)
        # Get the font family name for use in StyleSheet
        font_family = self.custom_font.family() if self.custom_font else "Squares-Bold"
        self.tab_widget.setStyleSheet(f"""
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
        self.createGeneralTab()
        self.createAppearanceTab()
        self.createNewsTab()

        # Add the tab widget to the layout
        layout.addWidget(self.tab_widget)

    def createGeneralTab(self):
        # Create the General tab
        general_tab = QWidget()
        general_layout = QVBoxLayout(general_tab)
        general_layout.setAlignment(Qt.AlignTop)
        general_layout.setContentsMargins(20, 20, 20, 20)
        general_layout.setSpacing(15)

        # Add title
        title_label = QLabel("Auto-Start Exodia Assistant")
        title_label.setFont(self.custom_font)
        # Get the font family name for use in StyleSheet
        font_family = self.custom_font.family() if self.custom_font else "Squares-Bold"
        title_label.setStyleSheet(f"color: #00B0C8; font-family: '{font_family}'; font-size: 24px;")
        general_layout.addWidget(title_label)

        # Add separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("background-color: #00B0C8;")
        general_layout.addWidget(separator)

        # Auto-start setting
        auto_start_layout = QHBoxLayout()
        auto_start_label = QLabel("Auto-start Assistant:")
        # Get the font family name for use in StyleSheet
        font_family = self.custom_font.family() if self.custom_font else "Squares-Bold"
        auto_start_label.setStyleSheet(f"color: white; font-family: '{font_family}'; font-size: 18px;")
        auto_start_layout.addWidget(auto_start_label)

        self.toggle_button = QPushButton('', general_tab)
        self.toggle_button.setFixedSize(100, 40)
        self.updateToggleButtonStyle()
        self.toggle_button.clicked.connect(self.toggleAutoStart)
        auto_start_layout.addWidget(self.toggle_button)
        auto_start_layout.addStretch()

        general_layout.addLayout(auto_start_layout)

        # Add the tab to the tab widget
        self.tab_widget.addTab(general_tab, "Auto-Start")

    def createAppearanceTab(self):
        # Create the Appearance tab
        appearance_tab = QWidget()
        appearance_layout = QVBoxLayout(appearance_tab)
        appearance_layout.setAlignment(Qt.AlignTop)
        appearance_layout.setContentsMargins(20, 20, 20, 20)
        appearance_layout.setSpacing(15)

        # Add title
        title_label = QLabel("Appearance Settings (In the Development stage)")
        title_label.setFont(self.custom_font)
        # Get the font family name for use in StyleSheet
        font_family = self.custom_font.family() if self.custom_font else "Squares-Bold"
        title_label.setStyleSheet(f"color: #00B0C8; font-family: '{font_family}'; font-size: 24px;")
        appearance_layout.addWidget(title_label)

        # Add separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("background-color: #00B0C8;")
        appearance_layout.addWidget(separator)

        # Theme setting
        theme_layout = QHBoxLayout()
        theme_label = QLabel("Theme:")
        # Get the font family name for use in StyleSheet
        font_family = self.custom_font.family() if self.custom_font else "Squares-Bold"
        theme_label.setStyleSheet(f"color: white; font-family: '{font_family}'; font-size: 18px;")
        theme_layout.addWidget(theme_label)

        theme_combo = QComboBox()
        theme_combo.addItems(["Dark", "Light"])
        theme_combo.setCurrentText("Dark" if self.theme == "dark" else "Light")
        # Get the font family name for use in StyleSheet
        font_family = self.custom_font.family() if self.custom_font else "Squares-Bold"
        theme_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: #151A21;
                color: white;
                border: 1px solid #00B0C8;
                border-radius: 5px;
                padding: 5px;
                min-width: 100px;
                font-family: '{font_family}';
                font-size: 16px;
            }}
            QComboBox::drop-down {{
                border: none;
            }}
            QComboBox QAbstractItemView {{
                background-color: #151A21;
                color: white;
                selection-background-color: #00B0C8;
                font-family: '{font_family}';
            }}
        """)
        theme_combo.currentTextChanged.connect(self.changeTheme)
        theme_layout.addWidget(theme_combo)
        theme_layout.addStretch()

        appearance_layout.addLayout(theme_layout)

        # Font size setting
        font_size_layout = QHBoxLayout()
        font_size_label = QLabel("Font Size:")
        # Get the font family name for use in StyleSheet
        font_family = self.custom_font.family() if self.custom_font else "Squares-Bold"
        font_size_label.setStyleSheet(f"color: white; font-family: '{font_family}'; font-size: 18px;")
        font_size_layout.addWidget(font_size_label)

        font_size_slider = QSlider(Qt.Horizontal)
        font_size_slider.setMinimum(12)
        font_size_slider.setMaximum(24)
        font_size_slider.setValue(self.font_size)
        font_size_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                border: 1px solid #00B0C8;
                height: 8px;
                background: #151A21;
                margin: 2px 0;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #00B0C8;
                border: 1px solid #00B0C8;
                width: 18px;
                margin: -2px 0;
                border-radius: 9px;
            }
        """)
        font_size_slider.valueChanged.connect(self.changeFontSize)
        font_size_layout.addWidget(font_size_slider)

        font_size_value = QLabel(str(self.font_size))
        # Get the font family name for use in StyleSheet
        font_family = self.custom_font.family() if self.custom_font else "Squares-Bold"
        font_size_value.setStyleSheet(f"color: white; font-family: '{font_family}'; font-size: 18px;")
        font_size_slider.valueChanged.connect(lambda value: font_size_value.setText(str(value)))
        font_size_layout.addWidget(font_size_value)

        appearance_layout.addLayout(font_size_layout)

        # Add the tab to the tab widget
        self.tab_widget.addTab(appearance_tab, "Appearance")

    def createNewsTab(self):
        # Create the News tab
        news_tab = QWidget()
        news_layout = QVBoxLayout(news_tab)
        news_layout.setAlignment(Qt.AlignTop)
        news_layout.setContentsMargins(20, 20, 20, 20)
        news_layout.setSpacing(15)

        # Add title
        title_label = QLabel("Change Profile Picture")
        title_label.setFont(self.custom_font)
        # Get the font family name for use in StyleSheet
        font_family = self.custom_font.family() if self.custom_font else "Squares-Bold"
        title_label.setStyleSheet(f"color: #00B0C8; font-family: '{font_family}'; font-size: 24px;")
        news_layout.addWidget(title_label)

        # Add separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("background-color: #00B0C8;")
        news_layout.addWidget(separator)

        # Add Profile Picture buttons
        buttons_layout = QHBoxLayout()

        # Create the "Change SDDM User Picture" button
        sddm_button = QPushButton("Change SDDM User Picture")
        sddm_button.setFixedSize(240, 40)
        # Get the font family name for use in StyleSheet
        font_family = self.custom_font.family() if self.custom_font else "Squares-Bold"
        sddm_button.setStyleSheet(f"""
            QPushButton {{
                background-color: #00B0C8;
                color: white;
                font-family: '{font_family}';
                font-size: 16px;
                font-weight: bold;
                border-radius: 5px;
            }}
            QPushButton:hover {{
                background-color: #008B9E;
            }}
            QPushButton:pressed {{
                background-color: #005F78;
            }}
        """)
        sddm_button.clicked.connect(self.change_sddm_user_picture)
        buttons_layout.addWidget(sddm_button)

        # Create the "Change Profile Picture" button
        profile_button = QPushButton("Change Profile Picture")
        profile_button.setFixedSize(240, 40)
        profile_button.setStyleSheet(f"""
            QPushButton {{
                background-color: #00B0C8;
                color: white;
                font-family: '{font_family}';
                font-size: 16px;
                font-weight: bold;
                border-radius: 5px;
            }}
            QPushButton:hover {{
                background-color: #008B9E;
            }}
            QPushButton:pressed {{
                background-color: #005F78;
            }}
        """)
        profile_button.clicked.connect(self.change_profile_picture)
        buttons_layout.addWidget(profile_button)

        buttons_layout.addStretch()
        news_layout.addLayout(buttons_layout)

        # Add the tab to the tab widget
        self.tab_widget.addTab(news_tab, "Profile Pictures")

    def updateToggleButtonStyle(self):
        # Get the font family name for use in StyleSheet
        font_family = self.custom_font.family() if self.custom_font else "Squares-Bold"
        if self.is_auto_start:
            self.toggle_button.setText('ON')
            self.toggle_button.setStyleSheet(f"""
                QPushButton {{
                    background-color: #00B0C8;
                    color: white;
                    font-family: '{font_family}';
                    font-size: 18px;
                    font-weight: bold;
                    border-radius: 5px;
                }}
            """)
        else:
            self.toggle_button.setText('OFF')
            self.toggle_button.setStyleSheet(f"""
                QPushButton {{
                    background-color: #151A21;
                    color: white;
                    font-family: '{font_family}';
                    font-size: 18px;
                    font-weight: bold;
                    border-radius: 5px;
                    border: 1px solid #00B0C8;
                }}
            """)

    def toggleAutoStart(self):
        self.is_auto_start = not self.is_auto_start
        self.updateToggleButtonStyle()
        self.saveAutoStartStatus()

    def changeTheme(self, theme_text):
        self.theme = "dark" if theme_text == "Dark" else "light"
        # Implementation for changing theme would go here
        print(f"Theme changed to: {self.theme}")

    def changeFontSize(self, size):
        self.font_size = size
        # Implementation for changing font size would go here
        print(f"Font size changed to: {self.font_size}")

    def changeRefreshRate(self, rate):
        self.news_refresh_rate = int(rate)
        # Implementation for changing news refresh rate would go here
        print(f"News refresh rate changed to: {self.news_refresh_rate} minutes")

    def saveAutoStartStatus(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as config_file:
                lines = config_file.readlines()

            with open(self.config_path, 'w') as config_file:
                for line in lines:
                    if 'exodia-assistant-auto-start' in line:
                        line = f'exodia-assistant-auto-start = {"true" if self.is_auto_start else "false"}\n'
                    config_file.write(line)
        else:
            with open(self.config_path, 'w') as config_file:
                config_file.write(f'exodia-assistant-auto-start = {"true" if self.is_auto_start else "false"}\n')

    def change_profile_picture(self):
        """
        Opens a file dialog to select an image and copies it to ~/.face
        """
        # Open the file dialog to select an image
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Images (*.png *.jpg *.jpeg *.bmp *.gif)")
        file_dialog.setViewMode(QFileDialog.Detail)

        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                source_file = selected_files[0]
                destination_file = os.path.expanduser("~/.face")

                try:
                    # Copy the selected image to ~/.face
                    shutil.copy2(source_file, destination_file)
                    QMessageBox.information(self, "Success", "Profile picture has been updated successfully.")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to update profile picture: {str(e)}")

    def change_sddm_user_picture(self):
        """
        Opens a file dialog to select an image and copies it to /usr/share/sddm/faces/${USER}.face.icon
        """
        # Open the file dialog to select an image
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Images (*.png *.jpg *.jpeg *.bmp *.gif)")
        file_dialog.setViewMode(QFileDialog.Detail)

        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                source_file = selected_files[0]

                # Get the current username
                username = getpass.getuser()
                destination_file = f"/usr/share/sddm/faces/{username}.face.icon"

                try:
                    # Copy the selected image to /usr/share/sddm/faces/${USER}.face.icon
                    # This operation might require root privileges
                    command = f"pkexec cp '{source_file}' '{destination_file}'"
                    result = os.system(command)

                    if result == 0:
                        QMessageBox.information(self, "Success", "SDDM user picture has been updated successfully.")
                    else:
                        QMessageBox.critical(self, "Error", "Failed to update SDDM user picture. Permission denied.")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to update SDDM user picture: {str(e)}")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.setBrush(QBrush(QColor("#0E1218")))
        painter.drawRect(self.rect())

        border_points = [
            QPoint(910, 100),  # Top center
            QPoint(940, 130),  # Top right
            QPoint(940, 440),  # Middle right
            QPoint(230, 440),  # Bottom center
            QPoint(200, 410),  # Bottom left
            QPoint(200, 100),  # Middle left
        ]
        border_polygon = QPolygon(border_points)

        border_pen = QPen(QColor("#00B0C8"))
        border_pen.setWidth(10)
        painter.setPen(border_pen)
        painter.drawPolygon(border_polygon)
