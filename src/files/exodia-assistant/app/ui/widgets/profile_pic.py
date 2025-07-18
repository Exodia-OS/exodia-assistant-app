#####################################
#                                   #
#  @author      : 00xWolf           #
#    GitHub    : @mmsaeed509       #
#    Developer : Mahmoud Mohamed   #
#  﫥  Copyright : Exodia OS         #
#                                   #
#####################################

import os
import yaml
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor, QRegion, QPixmap, QPen
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainterPath
from config import DEFAULT_USER_AVATAR, SETTINGS_FILE_PATH


class ProfilePicture(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Set the geometry (position and size) of the internal window
        # self.setGeometry(x, y, width, height)
        self.setGeometry(30, 20, 150, 150)
        self.setAttribute(Qt.WA_TranslucentBackground)  # Make the background transparent
        self.radius = min(self.width(), self.height()) // 2
        self.image_path = self.loadProfilePicturePath()
        self.pixmap = QPixmap(self.image_path)

        # Check if the pixmap is loaded correctly
        if self.pixmap.isNull():
            print(f"Failed to load image from: {self.image_path}")

    def loadProfilePicturePath(self):
        """Load profile picture path from settings.yaml"""
        try:
            if os.path.exists(SETTINGS_FILE_PATH):
                with open(SETTINGS_FILE_PATH, 'r') as file:
                    settings = yaml.safe_load(file) or {}
                    profile_path = settings.get('profile_picture_path')
                    if profile_path and os.path.exists(profile_path):
                        return profile_path
        except Exception as e:
            print(f"Error loading profile picture path from settings: {e}")
        
        # Fallback to default avatar
        return DEFAULT_USER_AVATAR

    def refreshProfilePicture(self):
        """Refresh the profile picture from settings"""
        self.image_path = self.loadProfilePicturePath()
        self.pixmap = QPixmap(self.image_path)
        self.update()  # Trigger a repaint

    def createCustomMask(self):
        # Define a circular mask
        path = QPainterPath()
        path.addEllipse(0, 0, self.width(), self.height())
        mask = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(mask)  # Apply the mask to make the window circular
        return path  # Return the path for use in the paint event

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw the custom shape with the image fill if the pixmap is valid
        if not self.pixmap.isNull():
            # Get the bounding rectangle of the circular path
            bounding_rect = self.rect()

            # Scale the pixmap to fit the bounding rectangle of the circle
            scaled_pixmap = self.pixmap.scaled(
                bounding_rect.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
            )

            # Clip the painter to the circular region
            painter.setClipRegion(QRegion(self.createCustomMask().toFillPolygon().toPolygon()))

            # Calculate offsets to center the pixmap within the bounding rectangle
            offset_x = (bounding_rect.width() - scaled_pixmap.width()) // 2
            offset_y = (bounding_rect.height() - scaled_pixmap.height()) // 2

            # Draw the scaled pixmap centered within the circle
            painter.drawPixmap(offset_x, offset_y, scaled_pixmap)

        # Draw the border with the specified color
        pen = QPen(QColor("#00B0C8"), 5)  # Create a pen with the desired color and border width
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawEllipse(self.rect())  # Draw the circular border
