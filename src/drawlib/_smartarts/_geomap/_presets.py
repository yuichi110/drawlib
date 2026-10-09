# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Auto-generated preset target enumerations for GeoMap (do not edit manually)."""

from __future__ import annotations

from enum import StrEnum
from typing import Final


class World(StrEnum):
    """Preset global and regional world map identifiers."""

    All = "world:all"
    Africa = "world:africa"
    APAC = "world:apac"
    Asia = "world:asia"
    EastAsia = "world:east_asia"
    Europe = "world:europe"
    MiddleEast = "world:middle_east"
    NorthAmerica = "world:north_america"
    Oceania = "world:oceania"
    SouthAmerica = "world:south_america"
    SoutheastAsia = "world:southeast_asia"


class Countries(StrEnum):
    """Preset country map identifiers (Admin-1 states/prefectures)."""

    Afghanistan = "countries/afghanistan"
    Aland = "countries/aland"
    Albania = "countries/albania"
    Algeria = "countries/algeria"
    Andorra = "countries/andorra"
    Angola = "countries/angola"
    AntiguaAndBarbuda = "countries/antigua_and_barbuda"
    Argentina = "countries/argentina"
    Armenia = "countries/armenia"
    Aruba = "countries/aruba"
    Australia = "countries/australia"
    Austria = "countries/austria"
    Azerbaijan = "countries/azerbaijan"
    Bahrain = "countries/bahrain"
    Bangladesh = "countries/bangladesh"
    Barbados = "countries/barbados"
    Belarus = "countries/belarus"
    Belgium = "countries/belgium"
    Belize = "countries/belize"
    Benin = "countries/benin"
    Bhutan = "countries/bhutan"
    Bolivia = "countries/bolivia"
    BosniaAndHerzegovina = "countries/bosnia_and_herzegovina"
    Botswana = "countries/botswana"
    Brazil = "countries/brazil"
    Brunei = "countries/brunei"
    Bulgaria = "countries/bulgaria"
    BurkinaFaso = "countries/burkina_faso"
    Burundi = "countries/burundi"
    Cambodia = "countries/cambodia"
    Cameroon = "countries/cameroon"
    Canada = "countries/canada"
    CapeVerde = "countries/cape_verde"
    CentralAfricanRepublic = "countries/central_african_republic"
    Chad = "countries/chad"
    Chile = "countries/chile"
    China = "countries/china"
    Colombia = "countries/colombia"
    Comoros = "countries/comoros"
    Congo = "countries/congo"
    CostaRica = "countries/costa_rica"
    Croatia = "countries/croatia"
    Cuba = "countries/cuba"
    Curacao = "countries/curacao"
    Cyprus = "countries/cyprus"
    CzechRepublic = "countries/czech_republic"
    DRCongo = "countries/dr_congo"
    Denmark = "countries/denmark"
    Djibouti = "countries/djibouti"
    Dominica = "countries/dominica"
    DominicanRepublic = "countries/dominican_republic"
    EastTimor = "countries/east_timor"
    Ecuador = "countries/ecuador"
    Egypt = "countries/egypt"
    ElSalvador = "countries/el_salvador"
    EquatorialGuinea = "countries/equatorial_guinea"
    Eritrea = "countries/eritrea"
    Estonia = "countries/estonia"
    Eswatini = "countries/eswatini"
    Ethiopia = "countries/ethiopia"
    Fiji = "countries/fiji"
    Finland = "countries/finland"
    France = "countries/france"
    FrenchPolynesia = "countries/french_polynesia"
    Gabon = "countries/gabon"
    Georgia = "countries/georgia"
    Germany = "countries/germany"
    Ghana = "countries/ghana"
    Greece = "countries/greece"
    Greenland = "countries/greenland"
    Grenada = "countries/grenada"
    Guam = "countries/guam"
    Guatemala = "countries/guatemala"
    Guernsey = "countries/guernsey"
    Guinea = "countries/guinea"
    GuineaBissau = "countries/guinea_bissau"
    Guyana = "countries/guyana"
    Haiti = "countries/haiti"
    Honduras = "countries/honduras"
    HongKong = "countries/hong_kong"
    Hungary = "countries/hungary"
    Iceland = "countries/iceland"
    India = "countries/india"
    Indonesia = "countries/indonesia"
    Iran = "countries/iran"
    Iraq = "countries/iraq"
    Ireland = "countries/ireland"
    IsleOfMan = "countries/isle_of_man"
    Israel = "countries/israel"
    Italy = "countries/italy"
    IvoryCoast = "countries/ivory_coast"
    Jamaica = "countries/jamaica"
    Japan = "countries/japan"
    Jersey = "countries/jersey"
    Jordan = "countries/jordan"
    Kazakhstan = "countries/kazakhstan"
    Kenya = "countries/kenya"
    Kiribati = "countries/kiribati"
    Kosovo = "countries/kosovo"
    Kuwait = "countries/kuwait"
    Kyrgyzstan = "countries/kyrgyzstan"
    Laos = "countries/laos"
    Latvia = "countries/latvia"
    Lebanon = "countries/lebanon"
    Lesotho = "countries/lesotho"
    Liberia = "countries/liberia"
    Libya = "countries/libya"
    Liechtenstein = "countries/liechtenstein"
    Lithuania = "countries/lithuania"
    Luxembourg = "countries/luxembourg"
    Macau = "countries/macau"
    Madagascar = "countries/madagascar"
    Malawi = "countries/malawi"
    Malaysia = "countries/malaysia"
    Maldives = "countries/maldives"
    Mali = "countries/mali"
    Malta = "countries/malta"
    MarshallIslands = "countries/marshall_islands"
    Mauritania = "countries/mauritania"
    Mauritius = "countries/mauritius"
    Mexico = "countries/mexico"
    Micronesia = "countries/micronesia"
    Moldova = "countries/moldova"
    Monaco = "countries/monaco"
    Mongolia = "countries/mongolia"
    Montenegro = "countries/montenegro"
    Morocco = "countries/morocco"
    Mozambique = "countries/mozambique"
    Myanmar = "countries/myanmar"
    Namibia = "countries/namibia"
    Nauru = "countries/nauru"
    Nepal = "countries/nepal"
    Netherlands = "countries/netherlands"
    NewCaledonia = "countries/new_caledonia"
    NewZealand = "countries/new_zealand"
    Nicaragua = "countries/nicaragua"
    Niger = "countries/niger"
    Nigeria = "countries/nigeria"
    NorthKorea = "countries/north_korea"
    NorthMacedonia = "countries/north_macedonia"
    Norway = "countries/norway"
    Oman = "countries/oman"
    Pakistan = "countries/pakistan"
    Palau = "countries/palau"
    Palestine = "countries/palestine"
    Panama = "countries/panama"
    PapuaNewGuinea = "countries/papua_new_guinea"
    Paraguay = "countries/paraguay"
    Peru = "countries/peru"
    Philippines = "countries/philippines"
    Poland = "countries/poland"
    Portugal = "countries/portugal"
    PuertoRico = "countries/puerto_rico"
    Qatar = "countries/qatar"
    Romania = "countries/romania"
    Russia = "countries/russia"
    Rwanda = "countries/rwanda"
    SaintKittsAndNevis = "countries/saint_kitts_and_nevis"
    SaintLucia = "countries/saint_lucia"
    SaintVincent = "countries/saint_vincent"
    Samoa = "countries/samoa"
    SanMarino = "countries/san_marino"
    SaoTomeAndPrincipe = "countries/sao_tome_and_principe"
    SaudiArabia = "countries/saudi_arabia"
    Senegal = "countries/senegal"
    Serbia = "countries/serbia"
    Seychelles = "countries/seychelles"
    SierraLeone = "countries/sierra_leone"
    Singapore = "countries/singapore"
    SintMaarten = "countries/sint_maarten"
    Slovakia = "countries/slovakia"
    Slovenia = "countries/slovenia"
    SolomonIslands = "countries/solomon_islands"
    Somalia = "countries/somalia"
    Somaliland = "countries/somaliland"
    SouthAfrica = "countries/south_africa"
    SouthKorea = "countries/south_korea"
    SouthSudan = "countries/south_sudan"
    Spain = "countries/spain"
    SriLanka = "countries/sri_lanka"
    Sudan = "countries/sudan"
    Suriname = "countries/suriname"
    Sweden = "countries/sweden"
    Switzerland = "countries/switzerland"
    Syria = "countries/syria"
    Taiwan = "countries/taiwan"
    Tajikistan = "countries/tajikistan"
    Tanzania = "countries/tanzania"
    Thailand = "countries/thailand"
    TheBahamas = "countries/the_bahamas"
    TheGambia = "countries/the_gambia"
    Togo = "countries/togo"
    Tonga = "countries/tonga"
    TrinidadAndTobago = "countries/trinidad_and_tobago"
    Tunisia = "countries/tunisia"
    Turkey = "countries/turkey"
    TurkishRepublicOfNorthernCyprus = "countries/turkish_republic_of_northern_cyprus"
    Turkmenistan = "countries/turkmenistan"
    Tuvalu = "countries/tuvalu"
    Uganda = "countries/uganda"
    Ukraine = "countries/ukraine"
    UnitedArabEmirates = "countries/united_arab_emirates"
    UnitedKingdom = "countries/united_kingdom"
    UnitedStates = "countries/united_states"
    UnitedStatesVirginIslands = "countries/united_states_virgin_islands"
    Uruguay = "countries/uruguay"
    Uzbekistan = "countries/uzbekistan"
    Vanuatu = "countries/vanuatu"
    VaticanCity = "countries/vatican_city"
    Venezuela = "countries/venezuela"
    Vietnam = "countries/vietnam"
    WesternSahara = "countries/western_sahara"
    Yemen = "countries/yemen"
    Zambia = "countries/zambia"
    Zimbabwe = "countries/zimbabwe"


class Cities(StrEnum):
    """Preset city/metropolitan map identifiers (wards/districts)."""

    Australia_Sydney = "cities/australia_sydney"
    China_HongKong = "cities/china_hong_kong"
    China_Shanghai = "cities/china_shanghai"
    France_Paris = "cities/france_paris"
    Germany_Berlin = "cities/germany_berlin"
    Italy_Rome = "cities/italy_rome"
    Japan_Kyoto = "cities/japan_kyoto"
    Japan_Osaka = "cities/japan_osaka"
    Japan_Tokyo = "cities/japan_tokyo"
    Singapore_Singapore = "cities/singapore_singapore"
    SouthKorea_Seoul = "cities/south_korea_seoul"
    Taiwan_Taipei = "cities/taiwan_taipei"
    UnitedKingdom_London = "cities/united_kingdom_london"
    UnitedStates_LosAngeles = "cities/united_states_los_angeles"
    UnitedStates_NewYork = "cities/united_states_new_york"
    UnitedStates_SanFrancisco = "cities/united_states_san_francisco"


PRESET_DEFAULT_RANGES: Final[dict[str, tuple[tuple[float, float], tuple[float, float]]]] = {
    "cities/japan_tokyo": ((138.9, 139.95), (35.5, 35.92)),
    "cities/united_states_san_francisco": ((-122.53, -122.35), (37.7, 37.84)),
    "countries/australia": ((112.0, 154.5), (-44.0, -10.0)),
    "countries/chile": ((-76.0, -66.0), (-56.0, -17.0)),
    "countries/denmark": ((8.0, 15.3), (54.5, 58.0)),
    "countries/ecuador": ((-81.5, -75.0), (-5.2, 1.6)),
    "countries/fiji": ((176.8, 180.0), (-21.0, -16.0)),
    "countries/france": ((-5.5, 10.0), (41.0, 51.5)),
    "countries/japan": ((127.0, 146.0), (26.0, 46.0)),
    "countries/kiribati": ((172.0, 177.0), (-3.0, 4.0)),
    "countries/netherlands": ((3.2, 7.3), (50.7, 53.6)),
    "countries/new_zealand": ((166.0, 179.0), (-47.5, -34.0)),
    "countries/norway": ((4.0, 31.5), (57.8, 71.5)),
    "countries/portugal": ((-9.6, -6.1), (36.8, 42.2)),
    "countries/russia": ((19.0, 180.0), (41.0, 82.0)),
    "countries/south_africa": ((16.0, 33.2), (-35.0, -22.0)),
    "countries/spain": ((-9.5, 4.5), (35.8, 44.0)),
    "countries/united_kingdom": ((-8.5, 2.2), (49.8, 61.0)),
    "countries/united_states": ((-126.0, -66.0), (24.0, 50.0)),
    "world/world": ((-180.0, 180.0), (-60.0, 84.0)),
    "world:africa": ((-20.0, 53.0), (-36.0, 38.0)),
    "world:all": ((-180.0, 180.0), (-60.0, 84.0)),
    "world:apac": ((65.0, 180.0), (-48.0, 55.0)),
    "world:asia": ((25.0, 150.0), (-12.0, 56.0)),
    "world:east_asia": ((73.0, 146.5), (18.0, 54.0)),
    "world:europe": ((-25.0, 45.0), (34.0, 72.0)),
    "world:middle_east": ((24.0, 64.0), (12.0, 43.5)),
    "world:north_america": ((-170.0, -50.0), (5.0, 75.0)),
    "world:oceania": ((110.0, 180.0), (-48.0, 0.0)),
    "world:south_america": ((-85.0, -32.0), (-58.0, 15.0)),
    "world:southeast_asia": ((92.0, 142.0), (-11.5, 29.0)),
}


__all__ = [
    "PRESET_DEFAULT_RANGES",
    "Cities",
    "Countries",
    "World",
]
