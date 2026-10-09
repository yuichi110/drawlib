# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

from pathlib import Path

import pytest

from drawlib.canvas import canvas, clear, setup
from drawlib.smartarts import GeoMap
from drawlib.styles import Styles


class TestGeoMapPresets:
    def setup_method(self) -> None:
        clear()
        setup(width=160, height=100)

    def test_world_all_and_regional_presets(self) -> None:
        m = GeoMap(GeoMap.World.All, area_style=Styles.Neutral)
        areas = m.get_areas()
        assert len(areas) > 150
        assert "Japan" in areas

        m.set_area_styles(["Antarctica"], style=Styles.Transparent)
        m.set_area_styles(["JP", "日本"], style=Styles.PrimaryFlat)
        m.draw((10, 10), width=140, height=70)

        jp_xy = m.get_area_xy("Japan")
        assert 10.0 <= jp_xy[0] <= 150.0
        assert 10.0 <= jp_xy[1] <= 80.0
        assert len(canvas._artists) > 100

        # Regional World presets (e.g. Asia, EastAsia, Europe)
        clear()
        setup(width=160, height=100)
        m_asia = GeoMap(GeoMap.World.Asia, area_style=Styles.Neutral)
        asia_areas = m_asia.get_areas()
        assert "Japan" in asia_areas
        assert "India" in asia_areas
        assert "France" not in asia_areas
        m_asia.set_area_styles(["Japan", "Singapore"], style=Styles.PrimaryFlat)
        m_asia.draw((10, 10), width=140, height=80)
        assert len(canvas._artists) > 20

    def test_world_transparent_default_and_asia_crop(self) -> None:
        m = GeoMap(GeoMap.World.EastAsia, area_style=Styles.Transparent)
        m.set_area_styles(["China", "North Korea"], Styles.Neutral)
        m.set_area_styles(["South Korea", "Taiwan"], Styles.PrimaryNeutral)
        m.set_area_styles(["Japan", "Hong Kong"], Styles.PrimaryFlat)
        m.draw((10, 10), width=120, height=90, lon_range=(106, 146), lat_range=(18, 46))
        assert len(canvas._artists) == 6

    def test_countries_presets(self) -> None:
        m = GeoMap(GeoMap.Countries.Japan, area_style=Styles.Neutral, background_style=Styles.LightFlat)
        areas = m.get_areas()
        assert len(areas) == 47
        assert areas[0] == "Hokkaido"
        assert "Tokyo" in areas
        assert "Osaka" in areas
        assert areas[-1] == "Okinawa"

        m.set_area_styles(
            ["Ibaraki", "Tochigi", "Gunma", "Saitama", "Chiba", "Tokyo", "Kanagawa"],
            style=Styles.PrimaryNeutral,
        )
        m.set_area_styles(["Tokyo"], style=Styles.PrimaryFlat)
        m.set_area_styles(["大阪府"], style=Styles.SecondaryFlat)
        m.draw((10, 10), width=80, height=75)

        tokyo_xy = m.get_area_xy("Tokyo")
        osaka_xy = m.get_area_xy("Osaka")
        assert tokyo_xy[0] > osaka_xy[0]
        assert tokyo_xy[1] > osaka_xy[1]

        direct_xy = m.lonlat_to_xy(139.6917, 35.6895)
        assert abs(direct_xy[0] - tokyo_xy[0]) < 5.0
        assert abs(direct_xy[1] - tokyo_xy[1]) < 5.0

        # Verify global country preset (e.g. UnitedStates, Germany)
        m_us = GeoMap(GeoMap.Countries.UnitedStates, area_style=Styles.Neutral)
        assert "California" in m_us.get_areas()
        assert "New York" in m_us.get_areas()

        m_de = GeoMap(GeoMap.Countries.Germany, area_style=Styles.Neutral)
        assert "Berlin" in m_de.get_areas()

    def test_cities_presets_and_transparent_auto_zoom(self) -> None:
        m = GeoMap(GeoMap.Cities.Japan_Tokyo, area_style=Styles.Transparent)
        areas = m.get_areas()
        assert len(areas) == 62
        assert "Chiyoda" in areas
        assert "Shibuya" in areas

        wards_23 = areas[:23]
        m.set_area_styles(wards_23, style=Styles.Neutral)
        m.set_area_styles(["Chiyoda", "渋谷区", "Minato"], style=Styles.PrimaryFlat)
        m.draw((15, 15), width=60)
        shibuya_xy = m.get_area_xy("渋谷")
        chiyoda_xy = m.get_area_xy("Chiyoda")
        assert chiyoda_xy[0] > shibuya_xy[0]
        assert len(canvas._artists) == 23

        # Check other global city presets
        m_ny = GeoMap(GeoMap.Cities.UnitedStates_NewYork, area_style=Styles.Neutral)
        assert "Manhattan" in m_ny.get_areas()
        assert "Brooklyn" in m_ny.get_areas()

        m_berlin = GeoMap(GeoMap.Cities.Germany_Berlin, area_style=Styles.Neutral)
        assert "Mitte" in m_berlin.get_areas()


class TestGeoMapCustomAndValidation:
    def setup_method(self) -> None:
        clear()
        setup(width=100, height=100)

    def test_custom_geojson_dict_and_file(self) -> None:
        sample_geojson = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {"area_code": "A1", "name": "WestZone"},
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[[130.0, 30.0], [135.0, 30.0], [135.0, 35.0], [130.0, 35.0], [130.0, 30.0]]],
                    },
                },
                {
                    "type": "Feature",
                    "properties": {"area_code": "A2", "name": "EastZone"},
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[[135.0, 30.0], [140.0, 30.0], [140.0, 35.0], [135.0, 35.0], [135.0, 30.0]]],
                    },
                },
            ],
        }
        m = GeoMap(sample_geojson, id_key="area_code", area_style=Styles.Neutral)
        assert m.get_areas() == ["A1", "A2"]
        m.set_area_styles(["WestZone"], style=Styles.AccentFlat)
        m.draw((10, 10), height=40, lon_range=(129.0, 141.0), lat_range=(29.0, 36.0), scale=1.2)

        p1 = m.get_area_xy("A1")
        p2 = m.get_area_xy("A2")
        assert p2[0] > p1[0]

        okinawa_path = Path("docs/docs_src/_assets/geodata/okinawa.geojson")
        if okinawa_path.is_file():
            m_oki = GeoMap(okinawa_path, area_style=Styles.Neutral)
            assert "Naha" in m_oki.get_areas()

    def test_validation_errors(self) -> None:
        m = GeoMap(GeoMap.Cities.Japan_Tokyo, area_style=Styles.Neutral)
        with pytest.raises(RuntimeError):
            m.get_area_xy("Chiyoda")
        with pytest.raises(RuntimeError):
            m.lonlat_to_xy(139.7, 35.6)
        with pytest.raises(ValueError, match="Unknown map area"):
            m.set_area_styles(["NonExistentPlace"], style=Styles.Primary)
        with pytest.raises(ValueError, match="At least one of 'width' or 'height'"):
            m.draw((10, 10))
