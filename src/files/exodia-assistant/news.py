#####################################
#                                   #
#  @author      : 00xWolf           #
#    GitHub    : @mmsaeed509       #
#    Developer : Mahmoud Mohamed   #
#  﫥  Copyright : Exodia OS         #
#                                   #
#####################################

import os
import json
import threading
from urllib.request import urlopen, Request
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea
from PyQt5.QtCore import Qt
import utils

class News(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Set the geometry (position and size) of the widget
        self.setGeometry(0, 0, 800, 600)
        self.setAttribute(Qt.WA_TranslucentBackground)  # Make the background transparent

        # Use predator font from utils.py
        self.predator_font = None
        self.predator_font = utils.loadPredatorFont()
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

        # GitHub API URL to list contents of the src directory
        self.github_api_url = "https://api.github.com/repos/Exodia-OS/exodia-assistant-news/contents/src"
        self.raw_base_url = "https://raw.githubusercontent.com/Exodia-OS/exodia-assistant-news/master/src/"
        self.local_news_dir = os.path.expanduser("/tmp/exodia-assistant/news/")
        self.local_news_path = os.path.join(self.local_news_dir, "News.html")

    def fetch_and_display_news(self, internal_window):
        """
        Fetches news content from GitHub and displays it in the internal window.
        
        Args:
            internal_window: The internal window object where the news content will be displayed
        """
        # Ensure a local directory exists
        os.makedirs(self.local_news_dir, exist_ok=True)

        # Display loading message
        internal_window.updateContent(
            "<div style='color: #00B0C8; text-align: center; font-size: 18px;'>Getting The Latest News...</div>")

        def fetch_and_cache_news():
            try:
                # Create request with User-Agent header (GitHub API requires this)
                req = Request(self.github_api_url)
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
                        file_url = f"{self.raw_base_url}{filename}"
                        local_path = os.path.join(self.local_news_dir, filename)

                        with urlopen(file_url) as response:
                            content = response.read()
                            with open(local_path, 'wb') as f:
                                f.write(content)
                    except Exception as e:
                        print(f"Failed to fetch {filename}: {str(e)}")
                        # Continue with other files even if one fails

                # After downloading, load the News.html if it exists
                if os.path.exists(self.local_news_path):
                    with open(self.local_news_path, 'r', encoding='utf-8') as f:
                        html_content = f.read()

                    # Format with predator font
                    formatted_html = f"<div style='font-family: {self.predator_font.family()};'>{html_content}</div>"
                    internal_window.updateContent(formatted_html)
                else:
                    # If News.html wasn't found, try to display any HTML file
                    html_files = [f for f in os.listdir(self.local_news_dir) if f.lower().endswith('.html')]
                    if html_files:
                        with open(os.path.join(self.local_news_dir, html_files[0]), 'r', encoding='utf-8') as f:
                            html_content = f.read()
                        formatted_html = f"<div style='font-family: {self.predator_font.family()};'>{html_content}</div>"
                        internal_window.updateContent(formatted_html)
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

                # Try to use a local cached version if available
                if os.path.exists(self.local_news_path):
                    try:
                        with open(self.local_news_path, 'r', encoding='utf-8') as f:
                            cached_content = f.read()
                        formatted_cached = f"<div style='font-family: {self.predator_font.family()};'>" \
                                           f"{cached_content}</div>"
                        internal_window.updateContent(formatted_cached + error_message)
                    except Exception as cache_error:
                        internal_window.updateContent(
                            f"<div style='color: red; text-align: center;'>" f"Failed to load cached news: {str(cache_error)}</div>")
                else:
                    internal_window.updateContent(error_message)

        # Start the background thread
        threading.Thread(target=fetch_and_cache_news, daemon=True).start()