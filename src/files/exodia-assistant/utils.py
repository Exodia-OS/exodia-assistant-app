import os, re

from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QFontDatabase, QFont, QPolygon, QRegion

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
    base_dir = os.path.dirname(__file__)
    html_file_path = os.path.join(base_dir, directory, filename)

    try:
        with open(html_file_path, "r", encoding="utf-8") as html_file:
            html_content = html_file.read()
    except FileNotFoundError:
        return f"""
        <div style="color: red; text-align: center; font-size: 18px; padding: 20px;">
            Error: Could not find the content file at <code>{html_file_path}</code>.
        </div>
        """
    except Exception as e:
        return f"""
        <div style="color: red; text-align: center; font-size: 18px; padding: 20px;">
            Error: An unexpected error occurred while reading the content file.<br>
            Details: {str(e)}
        </div>
        """

    # Function to replace ../something with file:// absolute path
    def replace_relative_path(match):
        quote = match.group(1)
        rel_path = match.group(2)
        abs_path = os.path.abspath(os.path.join(base_dir, rel_path))
        return f'{quote}file://{abs_path}'

    # Replace src="../..." and src='...'
    html_content = re.sub(r'(src=["\'])\.\.\/([^"\']+)', replace_relative_path, html_content)

    # Replace url("../...") and url('../...')
    html_content = re.sub(r'(url\(["\'])\.\.\/([^"\')]+)', replace_relative_path, html_content)

    # Inject font family if needed
    if "{}" in html_content:
        return html_content.format(font_family)
    else:
        return f"<div style='font-family: {font_family};'>{html_content}</div>"


def contentButtonMask():
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
