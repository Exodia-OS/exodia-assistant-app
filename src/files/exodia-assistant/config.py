#####################################
#                                   #
#  @author      : 00xWolf           #
#    GitHub    : @mmsaeed509       #
#    Developer : Mahmoud Mohamed   #
#  﫥  Copyright : Exodia OS         #
#                                   #
#####################################

"""
Centralized configuration for Exodia Assistant.
All global constants, paths, and environment settings should be defined here.
"""

import os
from typing import Final

# App Info
APP_NAME: Final[str]    = "Exodia OS Assistant"
APP_VERSION: Final[str] = "4.0.2"
APP_RELEASE: Final[str] = "2"

# Paths
BASE_DIR: Final[str]   = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR: Final[str] = os.path.join(BASE_DIR, "assets")
FONTS_DIR: Final[str]  = os.path.join(ASSETS_DIR, "fonts")
ICONS_DIR: Final[str]  = os.path.join(ASSETS_DIR, "icons")
IMGS_DIR: Final[str]   = os.path.join(ASSETS_DIR, "imgs")
HTML_DIR: Final[str]   = os.path.join(ASSETS_DIR, "html")

USER_CONFIG_DIR: Final[str]    = os.path.expanduser("~/.config/exodia-assistant")
ROLES_PROFILES_DIR: Final[str] = os.path.join(USER_CONFIG_DIR, "profiles")
ROLE_YAML_PATH: Final[str]     = os.path.join(USER_CONFIG_DIR, "role.yaml")
SETTINGS_PATH: Final[str]      = os.path.join(USER_CONFIG_DIR, "settings.yaml")

# Font
DEFAULT_FONT_FAMILY: Final[str] = "Squares-Bold"

# WM_CLASS
WM_CLASS: Final[str]   = "ExodiaOS Assistant"
WM_CLASS_2: Final[str] = "exodiaos-assistant"

# Environment
DEBUG: Final[bool] = bool(os.environ.get("EXODIA_DEBUG", False))

# Add more configuration constants as needed

