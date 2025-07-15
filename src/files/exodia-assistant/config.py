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

# App Info #
APP_NAME: Final[str]    = "ExodiaOS Assistant"
APP_VERSION: Final[str] = "4.1"
APP_RELEASE: Final[str] = "4"
APP_AUTHOR: Final[str]  = "Mahmoud Mohammed, @mmsaeed509 - 00xWolf"
APP_URL: Final[str]     = "https://github.com/Exodia-OS/exodia-assistant-app"
APP_LICENSE: Final[str] = "MIT License"

# Paths #
BASE_DIR: Final[str]   = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR: Final[str] = os.path.join(BASE_DIR, "assets")
FONTS_DIR: Final[str]  = os.path.join(ASSETS_DIR, "fonts")
ICONS_DIR: Final[str]  = os.path.join(ASSETS_DIR, "icons")
IMGS_DIR: Final[str]   = os.path.join(ASSETS_DIR, "imgs")
HTML_DIR: Final[str]   = os.path.join(ASSETS_DIR, "html")

USER_CONFIG_DIR: Final[str]     = os.path.expanduser("~/.config/exodia-assistant")
ROLES_PROFILES_DIR: Final[str]  = os.path.join(USER_CONFIG_DIR, "profiles")
ROLE_YAML_PATH: Final[str]      = os.path.join(USER_CONFIG_DIR, "role.yaml")
SETTINGS_FILE_PATH: Final[str]  = os.path.join(USER_CONFIG_DIR, "settings.yaml")
DEFAULT_USER_AVATAR: Final[str] = os.path.expanduser("~/.face")

# Font #
DEFAULT_FONT_FAMILY: Final[str] = "Squares-Bold"

# WM_CLASS #
WM_CLASS: Final[str]   = "ExodiaOS Assistant"
WM_CLASS_2: Final[str] = "exodiaos-assistant"

# Environment #
DEBUG: Final[bool] = bool(os.environ.get("EXODIA_DEBUG", False))
