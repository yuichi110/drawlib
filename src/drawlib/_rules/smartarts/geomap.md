# Drawlib GeoMap SmartArt Guidelines (`lib-smartarts-geomap`)

`GeoMap` renders vector geographical maps (`GeoMap.World.*`, `GeoMap.Countries.*`, `GeoMap.Cities.*`, or custom GeoJSON files/dicts) onto the Drawlib canvas without external GIS dependencies.

---

## 1. Geometry, Anchor & Sizing Rules

- **Anchor (`align`)**: Coordinate `xy=(x, y)` marks the **Bottom-Left** (`align="bottom_left"`, default) or **Center** (`align="center"`) of the map bounding box on the canvas.
- **Required Dimension (`width` or `height` Must Be Provided)**:
  Although `width` and `height` both default to `None` in `draw()`, **at least one of `width` or `height` MUST be passed**. Calling `m.draw()` with both `width=None` and `height=None` raises `ValueError: At least one of 'width' or 'height' must be provided to GeoMap.draw().`
- **Aspect Ratio & `background_style` Alignment**:
  - **Single-Dimension Sizing (Recommended for Natural Fit)**: Pass only `width=...` (or only `height=...`). `GeoMap` automatically computes the other dimension from the map's cosine-corrected geographical aspect ratio:
    $$\text{natural\_aspect} = \frac{(\text{max\_lon} - \text{min\_lon}) \cdot \cos(\text{mid\_lat})}{\text{max\_lat} - \text{min\_lat}}$$
    Both `background_style` and map polygons match edge-to-edge with zero letterboxing.
  - **Dual-Dimension Sizing (`width` AND `height` with `lon_range` / `lat_range`)**: When both `width` and `height` are specified, `background_style` fills the entire `width × height` outer box while map polygons are clipped to `lon_range` / `lat_range` and centered inside that box. To fill a fixed `width × height` frame edge-to-edge without ocean clipping, choose `lon_range` and `lat_range` so that $\text{natural\_aspect} \approx \text{width} / \text{height}$.
- **Coordinate Lookup Order (`draw()` First)**:
  - `get_area_xy(area)` and `lonlat_to_xy(lon, lat)` rely on the projection computed during `draw()` and **must be called AFTER `m.draw(...)`** (calling them before `draw()` raises `RuntimeError`).
  - To inspect valid area names before drawing, call `m.get_areas()` or inspect `m.data` (neither requires `draw()`). `set_area_styles()` and `get_area_xy()` accept canonical English names (`"Japan"`), ISO codes (`"JP"`, `"JPN"`), or Japanese names (`"日本"`).

---

## 2. Presets & Targets

- **`GeoMap.World`**: `All`, `Asia`, `Europe`, `NorthAmerica`, `SouthAmerica`, `Africa`, `Oceania`, `EastAsia`, `SoutheastAsia`, `APAC`, `MiddleEast`
- **`GeoMap.Countries`**: All 215 countries & territories (`Japan`, `UnitedStates`, `UnitedKingdom`, `Germany`, `France`, ...)
- **`GeoMap.Cities`**: 16 global metropolitan maps (`Australia_Sydney`, `China_HongKong`, `China_Shanghai`, `France_Paris`, `Germany_Berlin`, `Italy_Rome`, `Japan_Kyoto`, `Japan_Osaka`, `Japan_Tokyo`, `Singapore_Singapore`, `SouthKorea_Seoul`, `Taiwan_Taipei`, `UnitedKingdom_London`, `UnitedStates_LosAngeles`, `UnitedStates_NewYork`, `UnitedStates_SanFrancisco`)
- **Custom GeoJSON**: Any `.geojson` path (`str` or `Path`, e.g. `"_assets/geodata/okinawa.geojson"`) or parsed GeoJSON `dict`.

---

## 3. Constructor, `.data` Property & 5-Method API

```python
from drawlib.smartarts import GeoMap
from drawlib.styles import Styles

m = GeoMap(
    target: World | type[World] | Countries | Cities | str | Path | dict[str, Any],
    *,
    area_style: Style | None = Styles.Neutral,
    background_style: Style | None = None,
    id_key: str | None = None,
    name_key: str | None = None,
)
```

### Properties & Methods

- `m.data -> GeoData`: Returns the underlying normalized `GeoData` model containing map areas (`elements`), bounding boxes, and default viewport ranges.
- `m.get_areas() -> list[str]`: Returns the ordered list of canonical area names in the map (e.g. `["Hokkaido", ..., "Okinawa"]`).
- `m.set_area_styles(areas: list[str], style: Style) -> Self`: Assigns a custom `Style` to the specified map areas (pass `Styles.Transparent` to hide specific areas) and returns `self`.
- `m.draw(xy: tuple[float, float] = (0.0, 0.0), width: float | None = None, height: float | None = None, *, lon_range: tuple[float, float] | None = None, lat_range: tuple[float, float] | None = None, align: Literal["bottom_left", "center"] = "bottom_left", scale: float = 1.0) -> Self`: Renders the map onto the canvas and returns `self`.
- `m.get_area_xy(area: str) -> tuple[float, float]`: Returns the representative canvas `(x, y)` center coordinate for a named map area (must be called after `draw()`).
- `m.lonlat_to_xy(lon: float, lat: float) -> tuple[float, float]`: Converts a geographical `(lon, lat)` coordinate in decimal degrees to canvas `(x, y)` (must be called after `draw()`).

---

## 4. Production Example: Regional Map with Curved Trajectories & Pin Overlays

```drawlib code=show
from drawlib.canvas import save, setup
from drawlib.lines import line_curved
from drawlib.shapes import circle, rectangle
from drawlib.smartarts import GeoMap
from drawlib.styles import Styles
from drawlib.text import text

setup(width=115, height=70)

asia = GeoMap(
    GeoMap.World.Asia,
    area_style=Styles.White,
    background_style=Styles.PrimaryNeutral.patch(shape_r=1.5),
)
asia.set_area_styles(["China", "Vietnam", "Philippines"], Styles.AccentFlat)
asia.set_area_styles(["Japan"], Styles.PrimaryFlat)

# Match lon_range / lat_range aspect ratio (~1.75) to width / height (103 / 58)
asia.draw(
    xy=(6.0, 6.0),
    width=103.0,
    height=58.0,
    lon_range=(73, 148),
    lat_range=(16, 53),
    align="bottom_left",
    scale=1.0,
)

tokyo_xy = asia.lonlat_to_xy(139.69, 35.69)
for lon, lat, bend in [(116.40, 39.90, -0.18), (121.47, 31.23, 0.15), (105.83, 21.03, 0.18)]:
    src_xy = asia.lonlat_to_xy(lon, lat)
    line_curved(src_xy, tokyo_xy, bend=bend, arrow_head="->", style=Styles.AccentBold)
    circle(src_xy, radius=1.0, style=Styles.DarkFlat)

circle(tokyo_xy, radius=1.4, style=Styles.PrimaryFlat)
rectangle((tokyo_xy[0] - 5.0, tokyo_xy[1] + 8.0), width=24.0, height=5.8, style=Styles.PrimaryFlat.patch(shape_r=1.2))
text((tokyo_xy[0] - 5.0, tokyo_xy[1] + 8.0), "Tokyo Origin", style=Styles.WhiteBold.patch(text_size=10.5))
save()
```
