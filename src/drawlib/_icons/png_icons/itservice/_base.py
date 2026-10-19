# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""IT Service (GSI, Consulting, SIer, BPO, IT Staffing) icon provider."""

from __future__ import annotations

from drawlib._icons.png_icons._base import PngIconProvider

ITSERVICE_ALIASES: dict[str, str] = {
    "accenture_plc": "accenture",
    "acn": "accenture",
    "adecco_group": "adecco",
    "akkodis": "adecco",
    "bah": "booz_allen",
    "bain_and_company": "bain",
    "booz_allen_hamilton": "booz_allen",
    "boston_consulting_group": "bcg",
    "cgi_group": "cgi",
    "cts": "cognizant",
    "deloitte_touche": "deloitte",
    "dxc_technology": "dxc",
    "epam_systems": "epam",
    "ernst_and_young": "ey",
    "eviden": "atos",
    "experis": "manpower",
    "hcl": "hcltech",
    "hcl_technologies": "hcltech",
    "ibm_consulting": "ibm",
    "indra_sistemas": "indra",
    "larsen_toubro_infotech": "ltimindtree",
    "lti": "ltimindtree",
    "manpowergroup": "manpower",
    "mckinsey_and_company": "mckinsey",
    "mindtree": "ltimindtree",
    "minsait": "indra",
    "modis": "adecco",
    "nomura_research_institute": "nri",
    "nttdata": "ntt_data",
    "pricewaterhousecoopers": "pwc",
    "rackspace_technology": "rackspace",
    "randstad_digital": "randstad",
    "slalom_consulting": "slalom",
    "sopra": "sopra_steria",
    "tata_consultancy_services": "tcs",
    "techm": "tech_mahindra",
    "tek_systems": "teksystems",
    "tieto": "tietoevry",
    "tsystems": "t_systems",
}

ITSERVICE_PROVIDER = PngIconProvider(
    name="itservice",
    package_name="icon_itservice",
    asset_subdir="icons/itservice",
    aliases=ITSERVICE_ALIASES,
)

_write = ITSERVICE_PROVIDER.write
