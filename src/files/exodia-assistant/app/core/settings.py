import os
import shutil
import getpass
import yaml
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QBrush, QColor, QPen, QPolygon, QRegion
from PyQt5.QtWidgets import QMainWindow, QPushButton, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QCheckBox, QComboBox, QSlider, QScrollArea, QFrame, QFileDialog, QMessageBox
from ..utils import font_utils
from config import APP_VERSION, APP_RELEASE, SETTINGS_FILE_PATH


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
        self.theme = "dark"  # Default theme
        self.font_size = 18  # Default font size
        self.news_refresh_rate = 60  # Default refresh rate in minutes
        self.profile_picture_path = None  # Profile picture path from settings
        self.tab_widget = None
        self.loadSettings()  # Load settings from YAML file
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
        self.custom_font = font_utils.loadPredatorFont()
        if self.custom_font:
            self.custom_font.setPointSize(20)

    def getDefaultSettings(self):
        """Get default settings dictionary"""
        return {
            'auto-start': False,
            'theme': 'dark',
            'font_size': 18,
            'news_refresh_rate': 60,
            'profile_picture_path': None
        }

    def initializeDefaultSettings(self):
        """Initialize settings with default values"""
        defaults = self.getDefaultSettings()
        self.is_auto_start = defaults['auto-start']
        self.theme = defaults['theme']
        self.font_size = defaults['font_size']
        self.news_refresh_rate = defaults['news_refresh_rate']
        self.profile_picture_path = defaults['profile_picture_path']

    def loadSettings(self):
        """Load settings from YAML file"""
        try:
            # Ensure the config directory exists
            config_dir = os.path.dirname(SETTINGS_FILE_PATH)
            if not os.path.exists(config_dir):
                os.makedirs(config_dir, exist_ok=True)
                print(f"Created config directory: {config_dir}")

            if os.path.exists(SETTINGS_FILE_PATH):
                # Load existing settings
                with open(SETTINGS_FILE_PATH, 'r') as file:
                    settings = yaml.safe_load(file) or {}
                    
                # Load settings with defaults
                defaults = self.getDefaultSettings()
                self.is_auto_start = settings.get('auto-start', defaults['auto-start'])
                self.theme = settings.get('theme', defaults['theme'])
                self.font_size = settings.get('font_size', defaults['font_size'])
                self.news_refresh_rate = settings.get('news_refresh_rate', defaults['news_refresh_rate'])
                self.profile_picture_path = settings.get('profile_picture_path', defaults['profile_picture_path'])
                
                print(f"Settings loaded from: {SETTINGS_FILE_PATH}")
            else:
                # Create default settings file
                print(f"Settings file not found, creating default settings: {SETTINGS_FILE_PATH}")
                self.initializeDefaultSettings()
                self.saveSettings()
                
            print(f"Settings loaded: auto-start={self.is_auto_start}, theme={self.theme}, font_size={self.font_size}")
        except Exception as e:
            print(f"Error loading settings: {e}")
            print("Using default settings due to error")
            # Use defaults on error
            self.initializeDefaultSettings()

    def saveSettings(self):
        """Save settings to YAML file"""
        try:
            # Ensure directory exists
            config_dir = os.path.dirname(SETTINGS_FILE_PATH)
            os.makedirs(config_dir, exist_ok=True)
            
            settings = {
                'auto-start': self.is_auto_start,
                'theme': self.theme,
                'font_size': self.font_size,
                'news_refresh_rate': self.news_refresh_rate,
                'profile_picture_path': self.profile_picture_path
            }
            
            with open(SETTINGS_FILE_PATH, 'w') as file:
                yaml.dump(settings, file, default_flow_style=False, sort_keys=False)
                
            print(f"Settings saved to: {SETTINGS_FILE_PATH}")
            print(f"Settings content: {settings}")
        except Exception as e:
            print(f"Error saving settings to {SETTINGS_FILE_PATH}: {e}")
            print("Settings will be lost on app restart")

    def createSettingsBackup(self):
        """Create a backup of the current settings file"""
        try:
            if os.path.exists(SETTINGS_FILE_PATH):
                backup_path = f"{SETTINGS_FILE_PATH}.backup"
                import shutil
                shutil.copy2(SETTINGS_FILE_PATH, backup_path)
                print(f"Settings backup created: {backup_path}")
                return backup_path
        except Exception as e:
            print(f"Error creating settings backup: {e}")
        return None

    def restoreSettingsFromBackup(self):
        """Restore settings from backup if available"""
        try:
            backup_path = f"{SETTINGS_FILE_PATH}.backup"
            if os.path.exists(backup_path):
                import shutil
                shutil.copy2(backup_path, SETTINGS_FILE_PATH)
                print(f"Settings restored from backup: {backup_path}")
                return True
        except Exception as e:
            print(f"Error restoring settings from backup: {e}")
        return False

    def validateSettingsFile(self):
        """Validate the settings file and return True if valid"""
        try:
            if not os.path.exists(SETTINGS_FILE_PATH):
                return False
            
            with open(SETTINGS_FILE_PATH, 'r') as file:
                settings = yaml.safe_load(file)
                
            # Check if all required keys exist
            required_keys = ['auto-start', 'theme', 'font_size', 'news_refresh_rate', 'profile_picture_path']
            for key in required_keys:
                if key not in settings:
                    print(f"Missing required setting: {key}")
                    return False
                    
            return True
        except Exception as e:
            print(f"Settings file validation failed: {e}")
            return False



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

        # Add version display
        version_label = QLabel(f"v.{APP_VERSION}.{APP_RELEASE}")
        version_label.setFont(self.custom_font)
        # Get the font family name for use in StyleSheet
        font_family = self.custom_font.family() if self.custom_font else "Squares-Bold"
        version_label.setStyleSheet(f"color: #00B0C8; font-family: '{font_family}'; font-size: 18px;")
        general_layout.addWidget(version_label)

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
        self.tab_widget.addTab(news_tab, "Change Avatar")

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
        self.saveSettings()  # Save to YAML file

    def changeTheme(self, theme_text):
        self.theme = "dark" if theme_text == "Dark" else "light"
        # Implementation for changing theme would go here
        print(f"Theme changed to: {self.theme}")
        self.saveSettings()  # Save to YAML file

    def changeFontSize(self, size):
        self.font_size = size
        # Implementation for changing font size would go here
        print(f"Font size changed to: {self.font_size}")
        self.saveSettings()  # Save to YAML file

    def changeRefreshRate(self, rate):
        self.news_refresh_rate = int(rate)
        # Implementation for changing news refresh rate would go here
        print(f"News refresh rate changed to: {self.news_refresh_rate} minutes")
        self.saveSettings()  # Save to YAML file



    def change_profile_picture(self):
        """
        Opens a file dialog to select an image, saves the path to settings.yaml, and copies it to ~/.face
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
                    # Save the profile picture path to settings
                    self.profile_picture_path = source_file
                    self.saveSettings()
                    
                    # Copy the selected image to ~/.face
                    shutil.copy2(source_file, destination_file)
                    
                    # Refresh the profile picture widget if it exists
                    if hasattr(self.parent(), 'profile_picture'):
                        self.parent().profile_picture.refreshProfilePicture()
                    
                    QMessageBox.information(self, "Success", "Profile picture has been updated successfully and saved to settings.")
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
