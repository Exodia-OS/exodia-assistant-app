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
from PyQt5.QtCore import Qt, QPoint, QTimer
from PyQt5.QtGui import QPolygon, QRegion
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QScrollArea, QLineEdit
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
from urllib.request import urlopen, Request
import threading
import json

def createCustomButtonMaskKeybinding():
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
    font_path = os.path.join(os.path.dirname(__file__), './Fonts', 'Squares-Bold.otf')
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
        self.clearButtons()
        # Load and format the HTML content
        text = loadHTMLContent('./HTML-files', 'displayWelcomeContent.html', self.predator_font.family())

        # Update the content of the internal window
        self.internal_window.updateContent(text)


    def displayNewsContent(self):
        """
        Displays the news content fetched from a GitHub repository.
        Lists and downloads all files from the GitHub directory and stores them locally.
        If the fetch fails, it falls back to the local cached version.
        """
        # Clear previous buttons
        if not self.internal_window.layout():
            self.internal_window.setLayout(QVBoxLayout())
            self.clearButtons()
        else:
            self.clearButtons()

        # GitHub API URL to list contents of the src directory
        github_api_url = "https://api.github.com/repos/Exodia-OS/exodia-assistant-news/contents/src"
        raw_base_url = "https://raw.githubusercontent.com/Exodia-OS/exodia-assistant-news/master/src/"
        local_news_dir = os.path.expanduser("/tmp/exodia-assistant/news/")
        local_news_path = os.path.join(local_news_dir, "News.html")

        # Ensure local directory exists
        os.makedirs(local_news_dir, exist_ok=True)

        # Display loading message
        self.internal_window.updateContent(
            "<div style='color: #00B0C8; text-align: center; font-size: 18px;'>Getting The Latest News...</div>")

        def fetch_and_cache_news():
            try:
                # Create request with User-Agent header (GitHub API requires this)
                req = Request(github_api_url)
                req.add_header('User-Agent', 'Exodia-OS-Assistant')

                # Get directory listing
                with urlopen(req) as response:
                    directory_contents = json.loads(response.read().decode('utf-8'))

                # Filter for files (ignore subdirectories)
                files_to_download = [item['name'] for item in directory_contents if item['type'] == 'file']

                if not files_to_download:
                    raise Exception("No files found in the GitHub directory")

                # Download each file
                for filename in files_to_download:
                    try:
                        file_url = f"{raw_base_url}{filename}"
                        local_path = os.path.join(local_news_dir, filename)

                        with urlopen(file_url) as response:
                            content = response.read()
                            with open(local_path, 'wb') as f:
                                f.write(content)
                    except Exception as e:
                        print(f"Failed to fetch {filename}: {str(e)}")
                        # Continue with other files even if one fails

                # After downloading, load the News.html if it exists
                if os.path.exists(local_news_path):
                    with open(local_news_path, 'r', encoding='utf-8') as f:
                        html_content = f.read()

                    # Format with predator font
                    formatted_html = f"<div style='font-family: {self.predator_font.family()};'>{html_content}</div>"
                    self.internal_window.updateContent(formatted_html)
                else:
                    # If News.html wasn't found, try to display any HTML file
                    html_files = [f for f in os.listdir(local_news_dir) if f.lower().endswith('.html')]
                    if html_files:
                        with open(os.path.join(local_news_dir, html_files[0]), 'r', encoding='utf-8') as f:
                            html_content = f.read()
                        formatted_html = f"<div style='font-family: {self.predator_font.family()};'>{html_content}</div>"
                        self.internal_window.updateContent(formatted_html)
                    else:
                        raise Exception("No HTML files found in the downloaded content")

            except Exception as e:
                # Handle any errors
                error_message = f"""
                <div style="color: red; text-align: center; font-size: 18px; padding: 20px;">
                    Error: Failed to fetch news content. Details: {str(e)} <br>
                    Check your internet connection.
                </div>
                """

                # Try to use local cached version if available
                if os.path.exists(local_news_path):
                    try:
                        with open(local_news_path, 'r', encoding='utf-8') as f:
                            cached_content = f.read()
                        formatted_cached = f"<div style='font-family: {self.predator_font.family()};'>" \
                                           f"{cached_content}</div>"
                        self.internal_window.updateContent(formatted_cached + error_message)
                    except Exception as cache_error:
                        self.internal_window.updateContent(
                            f"<div style='color: red; text-align: center;'>" f"Failed to load cached news: {str(cache_error)}</div>")
                else:
                    self.internal_window.updateContent(error_message)

        # Start the background thread
        threading.Thread(target=fetch_and_cache_news, daemon=True).start()

    def displaySettingContent(self):

        self.clearButtons()  # Clear previous buttons
        # Load and format the HTML content
        text = loadHTMLContent('./HTML-files', 'displaySettingContent.html', self.predator_font.family())
        # Update the content of the internal window
        self.internal_window.updateContent(text)

    def displayRoleContent(self):

        self.clearButtons()  # Clear previous buttons
        # Load and format the HTML content
        text = loadHTMLContent('./HTML-files', 'displayRoleContent.html', self.predator_font.family())
        # Update the content of the internal window
        self.internal_window.updateContent(text)

    def displayDevelopersContent(self):

        self.clearButtons()  # Clear previous buttons
        # Load and format the HTML content
        text = loadHTMLContent('./HTML-files', 'displayDevelopersContent.html', self.predator_font.family())
        # Update the content of the internal window
        self.internal_window.updateContent(text)

    def displayKeybindingContent(self):

        text = ""

        # Base directory for HTML files
        html_dir = "./HTML-files/Keybinding"

        def clearLayout():
            """Clears the layout of the internal window."""
            while self.internal_window.layout().count():
                item = self.internal_window.layout().takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()

        def createCustomButton(label, html_file):
            """Creates a custom button widget with word-wrapped text and a custom shape."""
            button = QPushButton()
            button.setFixedSize(240, 100)
            button.setMask(createCustomButtonMaskKeybinding())
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
                f"color: white; font-family: '{self.predator_font.family()}'; font-size: 18px;"
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

            # Create the search input field
            search_input = QLineEdit()
            search_input.setPlaceholderText("Wiki Search...")
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
            self.internal_window.layout().addWidget(scroll_area)

        def showHTML(html_file):
            """Displays the content of the selected HTML file."""
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
                self.internal_window.layout().addWidget(top_widget)

                # Load the HTML content
                html_content = loadHTMLContent(html_dir, html_file, self.predator_font.family())

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

                content_label.setFont(self.predator_font)
                content_label.setStyleSheet(
                    f"color: #00B0C8; font-size: 18px; background-color: #151A21; padding: 10px;"
                    f"font-family: '{self.predator_font.family()}';"
                )
                content_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
                self.internal_window.layout().addWidget(scroll_area)

            except Exception as e:
                # Log the error and display a message
                print(f"Error loading HTML content: {e}")
                error_label = QLabel("Error: Unable to load content.")
                error_label.setStyleSheet("color: red; font-size: 18px;")
                self.internal_window.layout().addWidget(error_label)

        showButtons()
        self.internal_window.updateContent(text)

    def displayWikiContent(self):
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

            text_label = QLabel(label)
            text_label.setAlignment(Qt.AlignCenter)
            text_label.setWordWrap(True)
            text_label.setStyleSheet(
                f"color: white; font-family: '{self.predator_font.family()}'; font-size: 18px;"
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

            # Create the search input field
            search_input = QLineEdit()
            search_input.setPlaceholderText("Wiki Search...")
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

            # Create the search button
            search_button = QPushButton("Search")
            search_button.setFixedSize(100, 40)
            search_button.setStyleSheet(
                """
                QPushButton {
                    background-color: #006C7A;
                    color: white;
                    border: none;
                    font-size: 18px;
                }
                QPushButton:hover {
                    background-color: #004F59;
                }
                QPushButton:pressed {
                    background-color: #00343C;
                }
                """
            )
            search_button.setFont(self.predator_font)

            def performSearch():
                # Show buttons filtered by the search input
                keyword = search_input.text()
                showButtons(keyword)

            search_button.clicked.connect(performSearch)

            # Connect the "Enter" key press to the performSearch function
            search_input.returnPressed.connect(performSearch)

            # Add the search field and search button
            top_layout = QHBoxLayout()
            top_layout.addWidget(search_input, alignment=Qt.AlignLeft)
            # top_layout.addWidget(search_button, alignment=Qt.AlignRight)

            top_widget = QWidget()
            top_widget.setLayout(top_layout)
            self.internal_window.layout().addWidget(top_widget)

            # Define button labels and corresponding HTML file names
            tips_data = [
                ("PGP signature Error", "PGP-signature-Error.html"),
                ("Adding Music", "Adding-Music.html"),
                ("Set Keyboard Layout", "Set-Keyboard-Layout.html"),
                ("Changing SDDM User Picture", "Changing-SDDM-User-Picture.html"),
                ("Create Your Own Theme", "Create-Your-Own-Theme.html"),
                ("Setup Custom Monitors Config", "Setup-Custom-Monitors-Config.html"),
                ("Setup Polybar Modules", "Setup-Polybar-Modules.html"),
                ("Fix Cava Module", "Fix-Cava-Module.html"),
                ("Pacman Tips", "pacman-tips.html"),
                ("unable to lock database", "unable-to-lock-database.html"),
                ("Change Theme And Icons", "change-theme-and-icons.html"),
                ("BSPWM Themes", "bspwm-themes.html"),
                ("Change Font", "Change-Fonts.html")
            ]

            # Filter the buttons if a keyword is provided
            if keyword:
                tips_data = [item for item in tips_data if keyword.lower() in item[0].lower()]

            # Create a scrollable widget
            scroll_widget = QWidget()
            scroll_widget.setStyleSheet("background: transparent;")  # Make the scroll widget transparent
            scroll_layout = QVBoxLayout(scroll_widget)
            scroll_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins for a cleaner look

            # Add buttons to the scrollable widget
            row_layout = None
            for index, (label, html_file) in enumerate(tips_data):
                if index % 4 == 0:
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
            self.internal_window.layout().addWidget(scroll_area)

        def showHTML(html_file):
            """Displays the content of the selected HTML file."""
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
                self.internal_window.layout().addWidget(top_widget)

                # Load the HTML content
                html_content = loadHTMLContent(html_dir, html_file, self.predator_font.family())

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

                content_label.setFont(self.predator_font)
                content_label.setStyleSheet(
                    f"color: #00B0C8; font-size: 18px; background-color: #151A21; padding: 10px;"
                    f"font-family: '{self.predator_font.family()}';"
                )
                content_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
                self.internal_window.layout().addWidget(scroll_area)

            except Exception as e:
                # Log the error and display a message
                print(f"Error loading HTML content: {e}")
                error_label = QLabel("Error: Unable to load content.")
                error_label.setStyleSheet("color: red; font-size: 18px;")
                self.internal_window.layout().addWidget(error_label)

        showButtons()
        self.internal_window.updateContent(text)
