#####################################
#                                   #
#  @author      : 00xWolf           #
#    GitHub    : @mmsaeed509       #
#    Developer : Mahmoud Mohamed   #
#  﫥  Copyright : Exodia OS         #
#                                   #
#####################################

from PyQt5.QtWidgets import QApplication
from app.ui.windows.main_window import CustomShapeWindow  # Import the class directly
import config

if __name__ == '__main__':
    app = QApplication([])
    window = CustomShapeWindow()  # Create an instance of CustomShapeWindow
    window.show()
    app.exec_()
