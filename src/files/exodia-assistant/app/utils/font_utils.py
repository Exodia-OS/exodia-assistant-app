import os

from PyQt5.QtGui import QFontDatabase, QFont


def loadPredatorFont():
    # Load the font from the Fonts directory
    font_path = os.path.join(os.path.dirname(__file__), '../../assets/fonts', 'Squares-Bold.otf')
    font_id = QFontDatabase.addApplicationFont(font_path)
    if font_id == -1:
        print("Failed to load predator font.")
        return None
    else:
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        return QFont(font_family, 30, QFont.Bold)