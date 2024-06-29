# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

from drawlib.v0_1.apis import *

OUTPUT_DIR = "../../../output_tests/v0_1/fonts/brahmic/"


def test_bengali_sans():
    text(
        (50, 10),
        "Hello World. যেহেতু মানব পরিবারের সকল সদস্যের সমান ও অবিচ্ছেদ্য অধিকারসমূহ",
        style=TextStyle(font=FontBrahmic.BENGALI_SANSSERIF_LIGHT),
    )
    text(
        (50, 30),
        "Hello World. যেহেতু মানব পরিবারের সকল সদস্যের সমান ও অবিচ্ছেদ্য অধিকারসমূহ",
        style=TextStyle(font=FontBrahmic.BENGALI_SANSSERIF_REGULAR),
    )
    text(
        (50, 50),
        "Hello World. যেহেতু মানব পরিবারের সকল সদস্যের সমান ও অবিচ্ছেদ্য অধিকারসমূহ",
        style=TextStyle(font=FontBrahmic.BENGALI_SANSSERIF_BOLD),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_bengali_serif():
    text(
        (50, 10),
        "Hello World. যেহেতু মানব পরিবারের সকল সদস্যের সমান ও অবিচ্ছেদ্য অধিকারসমূহ",
        style=TextStyle(font=FontBrahmic.BENGALI_SERIF_LIGHT),
    )
    text(
        (50, 30),
        "Hello World. যেহেতু মানব পরিবারের সকল সদস্যের সমান ও অবিচ্ছেদ্য অধিকারসমূহ",
        style=TextStyle(font=FontBrahmic.BENGALI_SERIF_REGULAR),
    )
    text(
        (50, 50),
        "Hello World. যেহেতু মানব পরিবারের সকল সদস্যের সমান ও অবিচ্ছেদ্য অধিকারসমূহ",
        style=TextStyle(font=FontBrahmic.BENGALI_SERIF_BOLD),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_devanagari_sans():
    text(
        (50, 10),
        "Hello World. चूंकि मानव परिवार के सभी सदस्यों के जन्मजात गौरव और समान",
        style=TextStyle(font=FontBrahmic.DEVANAGARI_SANSSERIF_LIGHT),
    )
    text(
        (50, 30),
        "Hello World. चूंकि मानव परिवार के सभी सदस्यों के जन्मजात गौरव और समान",
        style=TextStyle(font=FontBrahmic.DEVANAGARI_SANSSERIF_REGULAR),
    )
    text(
        (50, 50),
        "Hello World. चूंकि मानव परिवार के सभी सदस्यों के जन्मजात गौरव और समान",
        style=TextStyle(font=FontBrahmic.DEVANAGARI_SANSSERIF_BOLD),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_devanagari_serif():
    text(
        (50, 10),
        "Hello World. चूंकि मानव परिवार के सभी सदस्यों के जन्मजात गौरव और समान",
        style=TextStyle(font=FontBrahmic.DEVANAGARI_SERIF_LIGHT),
    )
    text(
        (50, 30),
        "Hello World. चूंकि मानव परिवार के सभी सदस्यों के जन्मजात गौरव और समान",
        style=TextStyle(font=FontBrahmic.DEVANAGARI_SERIF_REGULAR),
    )
    text(
        (50, 50),
        "Hello World. चूंकि मानव परिवार के सभी सदस्यों के जन्मजात गौरव और समान",
        style=TextStyle(font=FontBrahmic.DEVANAGARI_SERIF_BOLD),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_tamil_sans():
    text(
        (50, 10),
        "Hello World. மனிதக் குடும்பத்தினைச் சேர்ந்த யாவரதும் உள்ளார்ந்த",
        style=TextStyle(font=FontBrahmic.TAMIL_SANSSERIF_LIGHT),
    )
    text(
        (50, 30),
        "Hello World. மனிதக் குடும்பத்தினைச் சேர்ந்த யாவரதும் உள்ளார்ந்த",
        style=TextStyle(font=FontBrahmic.TAMIL_SANSSERIF_REGULAR),
    )
    text(
        (50, 50),
        "Hello World. மனிதக் குடும்பத்தினைச் சேர்ந்த யாவரதும் உள்ளார்ந்த",
        style=TextStyle(font=FontBrahmic.TAMIL_SANSSERIF_BOLD),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_tamil_serif():
    text(
        (50, 10),
        "Hello World. மனிதக் குடும்பத்தினைச் சேர்ந்த யாவரதும் உள்ளார்ந்த",
        style=TextStyle(font=FontBrahmic.TAMIL_SERIF_LIGHT),
    )
    text(
        (50, 30),
        "Hello World. மனிதக் குடும்பத்தினைச் சேர்ந்த யாவரதும் உள்ளார்ந்த",
        style=TextStyle(font=FontBrahmic.TAMIL_SERIF_REGULAR),
    )
    text(
        (50, 50),
        "Hello World. மனிதக் குடும்பத்தினைச் சேர்ந்த யாவரதும் உள்ளார்ந்த",
        style=TextStyle(font=FontBrahmic.TAMIL_SERIF_BOLD),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_telugu_sans():
    text(
        (50, 10),
        "Hello World. మానవకుటంబమునందలి వ్యక్తులందరికిని గల ఆజన్మసిద్ధమైన ప్రతిపత్తిని,",
        style=TextStyle(font=FontBrahmic.TELUGU_SANSSERIF_LIGHT),
    )
    text(
        (50, 30),
        "Hello World. మానవకుటంబమునందలి వ్యక్తులందరికిని గల ఆజన్మసిద్ధమైన ప్రతిపత్తిని,",
        style=TextStyle(font=FontBrahmic.TELUGU_SANSSERIF_REGULAR),
    )
    text(
        (50, 50),
        "Hello World. మానవకుటంబమునందలి వ్యక్తులందరికిని గల ఆజన్మసిద్ధమైన ప్రతిపత్తిని,",
        style=TextStyle(font=FontBrahmic.TELUGU_SANSSERIF_BOLD),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_telugu_serif():
    text(
        (50, 10),
        "Hello World. మానవకుటంబమునందలి వ్యక్తులందరికిని గల ఆజన్మసిద్ధమైన ప్రతిపత్తిని,",
        style=TextStyle(font=FontBrahmic.TELUGU_SERIF_LIGHT),
    )
    text(
        (50, 30),
        "Hello World. మానవకుటంబమునందలి వ్యక్తులందరికిని గల ఆజన్మసిద్ధమైన ప్రతిపత్తిని,",
        style=TextStyle(font=FontBrahmic.TELUGU_SERIF_REGULAR),
    )
    text(
        (50, 50),
        "Hello World. మానవకుటంబమునందలి వ్యక్తులందరికిని గల ఆజన్మసిద్ధమైన ప్రతిపత్తిని,",
        style=TextStyle(font=FontBrahmic.TELUGU_SERIF_BOLD),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")
