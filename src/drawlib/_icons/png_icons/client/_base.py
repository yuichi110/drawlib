# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Client (browsers, OS, app stores, PC/mobile OEMs, smart devices, cars, peripherals) icon provider."""

from __future__ import annotations

from drawlib._icons.png_icons._base import PngIconProvider

CLIENT_ALIASES: dict[str, str] = {
    "abb_robotics": "abb",
    "amazon_alexa": "alexa",
    "amazon_echo": "alexa",
    "amazon_fire_tv": "fire_tv",
    "amazon_kindle": "kindle",
    "apple_app_store": "app_store",
    "apple_safari": "safari",
    "arc_browser": "arc",
    "ble": "bluetooth",
    "bmw_connected": "bmw",
    "brave_browser": "brave",
    "cat": "caterpillar",
    "chrome_os": "chromeos",
    "chromebook_os": "chromeos",
    "chromium_browser": "chromium",
    "deere": "john_deere",
    "dell_client": "dell",
    "echo": "alexa",
    "fanuc_robot": "fanuc",
    "finder": "macos",
    "fire_os": "amazon_fire",
    "fire_tablet": "amazon_fire",
    "fire_tv_stick": "fire_tv",
    "galaxy": "samsung",
    "google_android": "android",
    "google_chrome": "chrome",
    "google_fitbit": "fitbit",
    "google_play": "play_store",
    "google_play_store": "play_store",
    "honeywell_scanner": "honeywell",
    "hp_inc": "hp",
    "ipados": "ios",
    "iphone_brand": "apple",
    "kindle_fire": "amazon_fire",
    "komatsu_ltd": "komatsu",
    "lets_note": "panasonic",
    "linux_desktop": "linux",
    "logicool": "logitech",
    "mac": "apple",
    "mac_os": "macos",
    "meta_quest": "meta",
    "microsoft_edge": "edge",
    "mozilla_firefox": "firefox",
    "ms": "microsoft",
    "ms_edge": "edge",
    "ms_store": "microsoft_store",
    "ms_windows": "windows",
    "nintendo_switch": "nintendo",
    "oculus": "meta",
    "opera_browser": "opera",
    "play_station": "playstation",
    "ps": "playstation",
    "ps4": "playstation",
    "ps5": "playstation",
    "simatic": "siemens",
    "surface": "microsoft",
    "switch": "nintendo",
    "switch_bot": "switchbot",
    "tesla_motors": "tesla",
    "thinkpad": "lenovo",
    "tor": "tor_browser",
    "toughbook": "panasonic",
    "toyota_motor": "toyota",
    "ubuntu_desktop": "ubuntu",
    "usb_c": "usb",
    "vivaldi_browser": "vivaldi",
    "windows_11": "windows",
    "xbox_one": "xbox",
    "xbox_series": "xbox",
    "xperia": "sony",
    "yt": "youtube",
    "zebra_scanner": "zebra",
    "zenbook": "asus",
}

CLIENT_PROVIDER = PngIconProvider(
    name="client",
    package_name="icon_client",
    asset_subdir="icons/client",
    aliases=CLIENT_ALIASES,
)

_write = CLIENT_PROVIDER.write
