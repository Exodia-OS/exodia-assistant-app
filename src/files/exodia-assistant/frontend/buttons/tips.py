#####################################
#                                   #
#  @author      : 00xWolf           #
#    GitHub    : @mmsaeed509       #
#    Developer : Mahmoud Mohamed   #
#  﫥  Copyright : Exodia OS         #
#                                   #
#####################################

from PyQt5.QtWidgets import QPushButton

class TipsButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__("Tips", parent)  # Set the button label to "Tips"
        self.setStyleSheet("color: #00B0C8;")  # Customize the button's appearance
