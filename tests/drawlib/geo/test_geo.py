# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

import pytest

from drawlib.canvas import canvas, clear, setup
from drawlib.geo import Cities, Countries, GeoMap, World
from drawlib.styles import Styles


class TestGeoMapPresets:
    def setup_method(self) -> None:
        clear()
        setup(width=160, height=100)

    def test_world_preset_elements_and_draw(self) -> None:
        m = GeoMap(World, style=Styles.Neutral)
        elements = m.get_elements()
        assert len(elements) > 150
        assert "Japan" in elements
        groups = m.get_groups()
        assert "Asia" in groups
        assert "Europe" in groups

        m.exclude_groups("Antarctica")
        m.set_style("JP", style=Styles.PrimaryFlat)
        m.set_style("日本", style=Styles.PrimaryFlat)
        m.draw((10, 10), width=140, height=70)

        jp_xy = m.get_element_xy("Japan")
        assert 10.0 <= jp_xy[0] <= 150.0
        assert 10.0 <= jp_xy[1] <= 80.0
        assert len(canvas._artists) > 100

    def test_world_transparent_default_and_asia_crop(self) -> None:
        m = GeoMap(World, style=Styles.Transparent)
        m.set_style(["China", "North Korea", "Vietnam", "Laos"], Styles.Neutral)
        m.set_style(["South Korea", "Taiwan", "Philippines"], Styles.PrimaryNeutral)
        m.set_style(["Japan", "Hong Kong"], Styles.PrimaryFlat)
        m.draw((10, 10), width=120, height=90, lon_range=(106, 146), lat_range=(18, 46))
        # Only the 8 styled countries intersecting the viewport are added as PathPatch artists
        assert len(canvas._artists) == 8

    def test_japan_preset_elements_and_coordinates(self) -> None:
        m = GeoMap(Countries.Japan, style=Styles.Neutral, background_style=Styles.LightFlat)
        elements = m.get_elements()
        assert len(elements) == 47
        assert elements[0] == "Hokkaido"
        assert "Tokyo" in elements
        assert "Osaka" in elements
        assert elements[-1] == "Okinawa"

        groups = m.get_groups()
        assert "Kanto" in groups
        assert "Kansai" in groups

        m.set_group_style("Kanto", style=Styles.PrimaryNeutral)
        m.set_styles({"Tokyo": Styles.PrimaryFlat, "大阪府": Styles.SecondaryFlat})
        m.draw((10, 10), width=80, height=75)

        tokyo_xy = m.get_element_xy("Tokyo")
        osaka_xy = m.get_element_xy("Osaka")
        # Tokyo is east and north of Osaka
        assert tokyo_xy[0] > osaka_xy[0]
        assert tokyo_xy[1] > osaka_xy[1]

        direct_xy = m.lonlat_to_xy(139.6917, 35.6895)
        assert abs(direct_xy[0] - tokyo_xy[0]) < 5.0
        assert abs(direct_xy[1] - tokyo_xy[1]) < 5.0

    def test_tokyo_preset_23wards_filtering(self) -> None:
        m = GeoMap(Cities.Tokyo)
        assert len(m.get_elements()) == 62
        assert m.get_groups() == ["23wards", "tama", "islands"]

        m.include_groups("23wards")
        wards = m.get_elements()
        assert len(wards) == 23
        assert "Chiyoda" in wards
        assert "Shibuya" in wards

        m.set_style(["Chiyoda", "渋谷区", "Minato"], style=Styles.PrimaryFlat)
        m.draw((15, 15), width=60)
        shibuya_xy = m.get_element_xy("渋谷")
        chiyoda_xy = m.get_element_xy("Chiyoda")
        assert chiyoda_xy[0] > shibuya_xy[0]


class TestGeoMapCustomAndValidation:
    def setup_method(self) -> None:
        clear()
        setup(width=100, height=100)

    def test_custom_geojson_dict_and_sizing_modes(self) -> None:
        sample_geojson = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {"area_code": "A1", "name": "WestZone", "region": "West"},
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[[130.0, 30.0], [135.0, 30.0], [135.0, 35.0], [130.0, 35.0], [130.0, 30.0]]],
                    },
                },
                {
                    "type": "Feature",
                    "properties": {"area_code": "A2", "name": "EastZone", "region": "East"},
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[[135.0, 30.0], [140.0, 30.0], [140.0, 35.0], [135.0, 35.0], [135.0, 30.0]]],
                    },
                },
            ],
        }
        m = GeoMap(sample_geojson, id_key="area_code", style=Styles.Neutral)
        assert m.get_elements() == ["A1", "A2"]
        m.set_style("WestZone", style=Styles.AccentFlat)
        m.draw((10, 10), height=40, lon_range=(129.0, 141.0), lat_range=(29.0, 36.0), scale=1.2)

        p1 = m.get_element_xy("A1")
        p2 = m.get_element_xy("A2")
        assert p2[0] > p1[0]

        m.include_elements("A1").exclude_elements("A2")
        assert m.get_elements() == ["A1"]

    def test_validation_errors(self) -> None:
        m = GeoMap(Cities.Tokyo, style=Styles.Neutral)
        with pytest.raises(RuntimeError):
            m.get_element_xy("Chiyoda")
        with pytest.raises(RuntimeError):
            m.lonlat_to_xy(139.7, 35.6)
        with pytest.raises(ValueError, match="Unknown map element"):
            m.set_style("NonExistentPlace", style=Styles.Primary)
        with pytest.raises(ValueError, match="Unknown map group"):
            m.include_groups("NonExistentGroup")
        with pytest.raises(ValueError, match="At least one of 'width' or 'height'"):
            m.draw((10, 10))
