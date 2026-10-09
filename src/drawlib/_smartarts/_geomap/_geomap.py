# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GeoMap component implementation for drawlib.smartarts."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any, Self

from matplotlib.patches import PathPatch
from matplotlib.path import Path as MplPath
from pydantic import validate_call

from drawlib._core.l2_types import Coordinate, PosFloat
from drawlib._core.l3_colors import ColorUtil
from drawlib._core.l3_styles import Style
from drawlib._core.l4_canvas import canvas, rectangle, transform
from drawlib._smartarts._geomap._loader import load_geodata
from drawlib._smartarts._geomap._projection import GeoProjection, clip_ring_to_bbox
from drawlib._smartarts._geomap._types import (
    Cities,
    Countries,
    GeoData,
    GeoElement,
    GeoPolygon,
    WorldPreset,
)
from drawlib.styles import Styles


def _normalize_str_list(items: str | Sequence[str]) -> list[str]:
    """Normalize a single string or sequence of strings into a list of strings."""
    if isinstance(items, str):
        return [items]
    return [str(it) for it in items]


def _get_map_patch_options(style: Style, fallback_border_style: Style | None = None) -> dict[str, Any]:
    """Build Matplotlib PathPatch keyword options from a drawlib Style."""
    if style.shape_fill_color is None:
        facecolor: tuple[float, float, float, float] | str = "none"
    else:
        raw_fill = ColorUtil.get_mplot_rgba(style.shape_fill_color, alpha=style.alpha)
        facecolor = "none" if raw_fill[3] <= 0.0 else raw_fill

    line_w = style.shape_line_width if style.shape_line_width is not None else 0.0
    line_col = style.shape_line_color
    line_style = style.shape_line_style if style.shape_line_style is not None else "solid"

    # When highlighting a region with a Flat fill style (e.g. Styles.PrimaryFlat),
    # preserve the map's boundary stroke so adjacent territories remain distinct.
    if facecolor != "none" and (line_w <= 0.0 or line_col is None) and fallback_border_style is not None:
        fb = fallback_border_style
        fb_w = fb.shape_line_width or 0.0
        if fb_w <= 0.0 or fb.shape_line_color is None or (fb.alpha is not None and fb.alpha <= 0.0):
            fb = Styles.Neutral
            fb_w = fb.shape_line_width or 0.0
        if fb_w > 0.0 and fb.shape_line_color is not None:
            line_w = fb_w
            line_col = fb.shape_line_color
            line_style = fb.shape_line_style or "solid"

    if line_col is None or line_w <= 0.0:
        edgecolor: tuple[float, float, float, float] | str = "none"
        eff_line_w = 0.0
    else:
        raw_edge = ColorUtil.get_mplot_rgba(line_col, alpha=style.alpha)
        edgecolor = "none" if raw_edge[3] <= 0.0 else raw_edge
        eff_line_w = line_w * 0.45

    return {
        "facecolor": facecolor,
        "edgecolor": edgecolor,
        "linewidth": eff_line_w,
        "linestyle": line_style,
        "joinstyle": "round",
        "capstyle": "round",
        "zorder": 1,
    }


def _build_element_mpl_path(
    polygons: tuple[GeoPolygon, ...],
    proj: GeoProjection,
) -> MplPath | None:
    """Clip and project element polygons into a single compound Matplotlib Path."""
    vertices: list[tuple[float, float]] = []
    codes: list[Any] = []

    for poly in polygons:
        clipped_ext = clip_ring_to_bbox(
            poly.exterior,
            proj.min_lon,
            proj.min_lat,
            proj.max_lon,
            proj.max_lat,
        )
        if len(clipped_ext) < 4:
            continue

        rings = [clipped_ext]
        for hole in poly.holes:
            clipped_hole = clip_ring_to_bbox(
                hole,
                proj.min_lon,
                proj.min_lat,
                proj.max_lon,
                proj.max_lat,
            )
            if len(clipped_hole) >= 4:
                rings.append(clipped_hole)

        for ring in rings:
            proj_pts = [proj.project_unscaled(lon, lat) for lon, lat in ring]
            vertices.append(proj_pts[0])
            codes.append(MplPath.MOVETO)
            for pt in proj_pts[1:-1]:
                vertices.append(pt)
                codes.append(MplPath.LINETO)
            vertices.append(proj_pts[0])
            codes.append(MplPath.CLOSEPOLY)

    if not vertices:
        return None
    return MplPath(vertices=vertices, codes=codes)


class GeoMap:
    """Geographical map component for rendering world, country, city, and custom GeoJSON maps.

    Supports preset targets (``World``, ``Countries.Japan``, ``Cities.Tokyo``) as well as
    custom GeoJSON file paths or dictionaries.

    Attributes:
        data: Normalized ``GeoData`` model containing map elements and bounding boxes.
    """

    @validate_call
    def __init__(
        self,
        target: WorldPreset | Countries | Cities | str | Path | dict[str, Any],
        *,
        style: Style | None = None,
        background_style: Style | None = None,
        id_key: str | None = None,
        name_key: str | None = None,
    ) -> None:
        """Initialize a GeoMap instance.

        Args:
            target: Preset target (``World``, ``Countries.Japan``, ``Cities.Tokyo``),
                path to a ``.geojson`` file, or a parsed GeoJSON dictionary.
            style: Default ``Style`` applied to all map elements. Defaults to ``Styles.Neutral``
                with a map-optimized thin border (``shape_line_width=0.6``) when omitted.
            background_style: Optional ``Style`` for the map bounding box background (e.g. ocean fill).
                Defaults to ``None`` (transparent background).
            id_key: Optional GeoJSON property key to use as element identifier for custom files.
            name_key: Optional GeoJSON property key to use as element display name for custom files.
        """
        if style is None:
            resolved_style = Styles.Neutral
        else:
            style.validate_for("shape")
            resolved_style = style

        if background_style is not None:
            background_style.validate_for("shape")

        self._data: GeoData = load_geodata(target, id_key=id_key, name_key=name_key)
        self._style: Style = resolved_style
        self._background_style: Style | None = background_style

        # Lookup indexes for case-insensitive and alias resolution
        self._alias_to_id: dict[str, str] = {}
        self._group_alias_to_group: dict[str, str] = {}
        for eid, elem in self._data.elements.items():
            for alias in elem.aliases:
                self._alias_to_id.setdefault(alias, eid)
            # Ensure exact canonical id and name always win
            self._alias_to_id[eid.lower()] = eid
            self._alias_to_id[elem.name.lower()] = eid
            if elem.group:
                self._group_alias_to_group[elem.group.lower()] = elem.group
                if elem.group_ja:
                    self._group_alias_to_group[elem.group_ja.lower()] = elem.group

        self._active_ids: set[str] = set(self._data.elements.keys())
        self._filtered: bool = False
        self._element_styles: dict[str, Style] = {}
        self._last_projection: GeoProjection | None = None

    @property
    def data(self) -> GeoData:
        """Return the underlying normalized GeoData model."""
        return self._data

    def _resolve_element_id(self, name_or_alias: str) -> str:
        """Resolve an element name, ISO code, or Japanese name to its canonical element ID."""
        key = name_or_alias.strip().lower()
        if key in self._alias_to_id:
            return self._alias_to_id[key]
        sample = ", ".join(list(self._data.elements.keys())[:8])
        raise ValueError(
            f"Unknown map element {name_or_alias!r} in dataset '{self._data.name}'. "
            f"Available elements include: [{sample}, ...]. Use get_elements() to inspect all."
        )

    def _resolve_group_name(self, group_name: str) -> str:
        """Resolve a group/region name (English or Japanese) to its canonical group name."""
        key = group_name.strip().lower()
        if key in self._group_alias_to_group:
            return self._group_alias_to_group[key]
        available = ", ".join(self.get_groups())
        raise ValueError(
            f"Unknown map group {group_name!r} in dataset '{self._data.name}'. "
            f"Available groups: [{available}]."
        )

    def get_elements(self) -> list[str]:
        """Return the list of active canonical element names in this map.

        Returns:
            list[str]: Ordered list of element names (e.g. ``["Hokkaido", ..., "Okinawa"]``).
        """
        return [eid for eid in self._data.elements if eid in self._active_ids]

    def get_groups(self) -> list[str]:
        """Return the list of available group/region names in this map.

        Returns:
            list[str]: Unique group names in order of appearance (e.g. ``["23wards", "tama", "islands"]``).
        """
        seen: dict[str, None] = {}
        for elem in self._data.elements.values():
            if elem.group and elem.group not in seen:
                seen[elem.group] = None
        return list(seen.keys())

    @validate_call
    def include_elements(self, elements: str | Sequence[str]) -> Self:
        """Restrict the map to render only the specified elements.

        Args:
            elements: Element name or sequence of element names to keep visible.

        Returns:
            Self: This GeoMap instance for method chaining.
        """
        resolved = {self._resolve_element_id(e) for e in _normalize_str_list(elements)}
        self._active_ids &= resolved
        self._filtered = True
        return self

    @validate_call
    def exclude_elements(self, elements: str | Sequence[str]) -> Self:
        """Exclude the specified elements from rendering.

        Args:
            elements: Element name or sequence of element names to hide.

        Returns:
            Self: This GeoMap instance for method chaining.
        """
        resolved = {self._resolve_element_id(e) for e in _normalize_str_list(elements)}
        self._active_ids -= resolved
        self._filtered = True
        return self

    @validate_call
    def include_groups(self, groups: str | Sequence[str]) -> Self:
        """Restrict the map to render only elements belonging to the specified groups.

        Args:
            groups: Group name or sequence of group names to keep (e.g. ``"23wards"``, ``"Kanto"``).

        Returns:
            Self: This GeoMap instance for method chaining.
        """
        target_groups = {self._resolve_group_name(g) for g in _normalize_str_list(groups)}
        keep = {eid for eid, elem in self._data.elements.items() if elem.group in target_groups}
        self._active_ids &= keep
        self._filtered = True
        return self

    @validate_call
    def exclude_groups(self, groups: str | Sequence[str]) -> Self:
        """Exclude elements belonging to the specified groups from rendering.

        Args:
            groups: Group name or sequence of group names to hide (e.g. ``"islands"``, ``"Antarctica"``).

        Returns:
            Self: This GeoMap instance for method chaining.
        """
        target_groups = {self._resolve_group_name(g) for g in _normalize_str_list(groups)}
        drop = {eid for eid, elem in self._data.elements.items() if elem.group in target_groups}
        self._active_ids -= drop
        self._filtered = True
        return self

    @validate_call
    def set_style(
        self,
        element: str | Sequence[str],
        style: Style,
    ) -> Self:
        """Assign a custom Style to one or more map elements.

        Args:
            element: Single element name (or alias/ISO/Japanese name) or sequence of element names.
            style: ``Style`` object to apply to the specified element(s).

        Returns:
            Self: This GeoMap instance for method chaining.
        """
        style.validate_for("shape")
        for item in _normalize_str_list(element):
            eid = self._resolve_element_id(item)
            self._element_styles[eid] = style
        return self

    @validate_call
    def set_styles(
        self,
        styles: Mapping[str, Style],
    ) -> Self:
        """Assign custom Styles to multiple map elements from a dictionary.

        Args:
            styles: Mapping from element name (or alias) to ``Style`` object.

        Returns:
            Self: This GeoMap instance for method chaining.
        """
        for elem_name, style in styles.items():
            self.set_style(elem_name, style)
        return self

    @validate_call
    def set_group_style(
        self,
        group: str | Sequence[str],
        style: Style,
    ) -> Self:
        """Assign a custom Style to all elements in one or more groups.

        Args:
            group: Single group name or sequence of group names (e.g. ``"Kanto"``, ``"23wards"``).
            style: ``Style`` object to apply to all elements in the group(s).

        Returns:
            Self: This GeoMap instance for method chaining.
        """
        style.validate_for("shape")
        target_groups = {self._resolve_group_name(g) for g in _normalize_str_list(group)}
        for eid, elem in self._data.elements.items():
            if elem.group in target_groups:
                self._element_styles[eid] = style
        return self

    def _compute_auto_ranges(
        self,
        active_elements: list[GeoElement],
    ) -> tuple[tuple[float, float], tuple[float, float]]:
        """Determine default (lon_range, lat_range) for the current active elements."""
        if not self._filtered and self._data.default_lon_range and self._data.default_lat_range:
            return self._data.default_lon_range, self._data.default_lat_range

        min_lon = min(e.bbox[0] for e in active_elements)
        min_lat = min(e.bbox[1] for e in active_elements)
        max_lon = max(e.bbox[2] for e in active_elements)
        max_lat = max(e.bbox[3] for e in active_elements)

        # When filtering (e.g. Kanto or Tokyo), clamp to preset mainland bounds unless all elements lie outside
        if self._data.default_lon_range and self._data.default_lat_range:
            d_lon0, d_lon1 = self._data.default_lon_range
            d_lat0, d_lat1 = self._data.default_lat_range
            in_bounds_lons: list[float] = []
            in_bounds_lats: list[float] = []
            for elem in active_elements:
                for poly in elem.polygons:
                    xs = [p[0] for p in poly.exterior]
                    ys = [p[1] for p in poly.exterior]
                    if max(xs) >= d_lon0 and min(xs) <= d_lon1 and max(ys) >= d_lat0 and min(ys) <= d_lat1:
                        in_bounds_lons.extend(max(d_lon0, min(d_lon1, x)) for x in xs)
                        in_bounds_lats.extend(max(d_lat0, min(d_lat1, y)) for y in ys)
            if in_bounds_lons and in_bounds_lats:
                min_lon, max_lon = min(in_bounds_lons), max(in_bounds_lons)
                min_lat, max_lat = min(in_bounds_lats), max(in_bounds_lats)

        pad_lon = max(0.01, (max_lon - min_lon) * 0.02)
        pad_lat = max(0.01, (max_lat - min_lat) * 0.02)
        return (min_lon - pad_lon, max_lon + pad_lon), (min_lat - pad_lat, max_lat + pad_lat)

    def _render_elements(
        self,
        active_elements: list[GeoElement],
        proj: GeoProjection,
    ) -> None:
        """Append projected PathPatch artists for all visible map elements."""
        default_elems = [e for e in active_elements if e.id not in self._element_styles]
        custom_elems = [e for e in active_elements if e.id in self._element_styles]

        default_opts = _get_map_patch_options(self._style)
        if default_opts["facecolor"] != "none" or default_opts["edgecolor"] != "none":
            for elem in default_elems:
                mpl_path = _build_element_mpl_path(elem.polygons, proj)
                if mpl_path is not None:
                    canvas._artists.append(PathPatch(mpl_path, **default_opts))

        for elem in custom_elems:
            custom_style = self._element_styles[elem.id]
            opts = _get_map_patch_options(custom_style, fallback_border_style=self._style)
            if opts["facecolor"] == "none" and opts["edgecolor"] == "none":
                continue
            mpl_path = _build_element_mpl_path(elem.polygons, proj)
            if mpl_path is not None:
                canvas._artists.append(PathPatch(mpl_path, **opts))

    @validate_call
    def draw(
        self,
        xy: tuple[float, float] = (0.0, 0.0),
        width: float | None = None,
        height: float | None = None,
        *,
        lon_range: tuple[float, float] | None = None,
        lat_range: tuple[float, float] | None = None,
        scale: float = 1.0,
    ) -> Self:
        """Render the map onto the active drawlib canvas.

        Args:
            xy: Bottom-left coordinate tuple ``(x, y)`` of the map bounding box on the canvas.
            width: Target width of the map bounding box (or ``None`` to auto-calculate from ``height``).
            height: Target height of the map bounding box (or ``None`` to auto-calculate from ``width``).
            lon_range: Optional ``(min_lon, max_lon)`` viewport range to crop/zoom the map.
            lat_range: Optional ``(min_lat, max_lat)`` viewport range to crop/zoom the map.
            scale: Proportional scale factor applied around ``xy`` (> 0). Defaults to 1.0.

        Returns:
            Self: This GeoMap instance for method chaining and coordinate lookup.
        """
        if width is not None and width <= 0:
            raise ValueError(f"width must be positive (> 0), got {width}.")
        if height is not None and height <= 0:
            raise ValueError(f"height must be positive (> 0), got {height}.")
        if scale <= 0:
            raise ValueError(f"scale must be positive (> 0), got {scale}.")

        active_elements = [elem for eid, elem in self._data.elements.items() if eid in self._active_ids]
        if not active_elements:
            raise ValueError("No active map elements remain to draw after filtering.")

        auto_lon, auto_lat = self._compute_auto_ranges(active_elements)
        eff_lon_range = lon_range if lon_range is not None else auto_lon
        eff_lat_range = lat_range if lat_range is not None else auto_lat

        proj = GeoProjection.create(
            xy=xy,
            width=width,
            height=height,
            lon_range=eff_lon_range,
            lat_range=eff_lat_range,
            scale=scale,
        )
        self._last_projection = proj

        with transform(origin=xy, scale=scale):
            if self._background_style is not None:
                bg_cx = proj.box_x + proj.box_width * 0.5
                bg_cy = proj.box_y + proj.box_height * 0.5
                rectangle(
                    (bg_cx, bg_cy),
                    width=proj.box_width,
                    height=proj.box_height,
                    style=self._background_style,
                )
            self._render_elements(active_elements, proj)

        return self

    @validate_call
    def lonlat_to_xy(self, lon: float, lat: float) -> tuple[float, float]:
        """Convert a geographical (lon, lat) coordinate to the canvas (x, y) of the last drawn map.

        Args:
            lon: Longitude in decimal degrees.
            lat: Latitude in decimal degrees.

        Returns:
            tuple[float, float]: Canvas coordinate ``(x, y)``.

        Raises:
            RuntimeError: If called before ``draw()`` has been executed.
        """
        if self._last_projection is None:
            raise RuntimeError("GeoMap.draw() must be called before querying canvas coordinates.")
        return self._last_projection.project_canvas(lon, lat)

    @validate_call
    def get_element_xy(self, element: str) -> tuple[float, float]:
        """Return the representative canvas (x, y) coordinate for a named map element.

        Args:
            element: Element name, ISO code, or Japanese name (e.g. ``"Tokyo"``, ``"Japan"``, ``"Chiyoda"``).

        Returns:
            tuple[float, float]: Canvas coordinate ``(x, y)`` of the element's interior center.

        Raises:
            RuntimeError: If called before ``draw()`` has been executed.
            ValueError: If ``element`` is not found in the map.
        """
        if self._last_projection is None:
            raise RuntimeError("GeoMap.draw() must be called before querying element canvas coordinates.")
        eid = self._resolve_element_id(element)
        elem = self._data.elements[eid]
        lon, lat = elem.center_lonlat
        return self._last_projection.project_canvas(lon, lat)


__all__ = ["GeoMap"]
