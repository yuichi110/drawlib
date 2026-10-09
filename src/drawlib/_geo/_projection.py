# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Map viewport projection, aspect-ratio fitting, and polygon clipping utilities."""

from __future__ import annotations

import math
from dataclasses import dataclass

Point2D = tuple[float, float]
Ring2D = tuple[Point2D, ...]


def _is_inside_edge(p: Point2D, edge: str, bound: float) -> bool:
    """Return True if point p lies inside the half-plane defined by edge and bound."""
    if edge == "left":
        return p[0] >= bound
    if edge == "right":
        return p[0] <= bound
    if edge == "bottom":
        return p[1] >= bound
    return p[1] <= bound


def _intersect_edge(p1: Point2D, p2: Point2D, edge: str, bound: float) -> Point2D:
    """Compute intersection point of segment p1->p2 with an axis-aligned boundary line."""
    x1, y1 = p1
    x2, y2 = p2
    if edge in {"left", "right"}:
        if abs(x2 - x1) < 1e-12:
            return (bound, y1)
        return (bound, y1 + ((bound - x1) / (x2 - x1)) * (y2 - y1))
    if abs(y2 - y1) < 1e-12:
        return (x1, bound)
    return (x1 + ((bound - y1) / (y2 - y1)) * (x2 - x1), bound)


def _clip_against_edge(
    pts: list[Point2D],
    edge: str,
    bound: float,
) -> list[Point2D]:
    """Clip a polygon vertex list against a single axis-aligned half-plane."""
    if not pts:
        return []

    out: list[Point2D] = []
    prev = pts[-1]
    prev_in = _is_inside_edge(prev, edge, bound)
    for curr in pts:
        curr_in = _is_inside_edge(curr, edge, bound)
        if curr_in:
            if not prev_in:
                out.append(_intersect_edge(prev, curr, edge, bound))
            out.append(curr)
        elif prev_in:
            out.append(_intersect_edge(prev, curr, edge, bound))
        prev = curr
        prev_in = curr_in
    return out


def clip_ring_to_bbox(
    ring: Ring2D,
    min_lon: float,
    min_lat: float,
    max_lon: float,
    max_lat: float,
) -> Ring2D:
    """Clip a closed (lon, lat) ring to an axis-aligned bounding box.

    Args:
        ring: Closed ring of (lon, lat) points.
        min_lon: Minimum longitude bound.
        min_lat: Minimum latitude bound.
        max_lon: Maximum longitude bound.
        max_lat: Maximum latitude bound.

    Returns:
        Clipped closed ring, or empty tuple if completely outside.
    """
    if len(ring) < 4:
        return ()

    xs = [p[0] for p in ring]
    ys = [p[1] for p in ring]
    r_min_x, r_max_x = min(xs), max(xs)
    r_min_y, r_max_y = min(ys), max(ys)

    if r_max_x < min_lon or r_min_x > max_lon or r_max_y < min_lat or r_min_y > max_lat:
        return ()
    if r_min_x >= min_lon and r_max_x <= max_lon and r_min_y >= min_lat and r_max_y <= max_lat:
        return ring

    pts = list(ring[:-1]) if ring[0] == ring[-1] else list(ring)
    pts = _clip_against_edge(pts, "left", min_lon)
    pts = _clip_against_edge(pts, "right", max_lon)
    pts = _clip_against_edge(pts, "bottom", min_lat)
    pts = _clip_against_edge(pts, "top", max_lat)

    if len(pts) < 3:
        return ()
    if pts[0] != pts[-1]:
        pts.append(pts[0])
    return tuple(pts)


@dataclass(frozen=True)
class GeoProjection:
    """Affine projection mapping (lon, lat) into a drawlib canvas bounding box."""

    min_lon: float
    min_lat: float
    max_lon: float
    max_lat: float
    cos_lat: float
    box_x: float
    box_y: float
    box_width: float
    box_height: float
    map_x: float
    map_y: float
    map_width: float
    map_height: float
    anchor_xy: tuple[float, float]
    scale: float

    @classmethod
    def create(
        cls,
        *,
        xy: tuple[float, float],
        width: float | None,
        height: float | None,
        lon_range: tuple[float, float],
        lat_range: tuple[float, float],
        scale: float = 1.0,
    ) -> GeoProjection:
        """Construct a GeoProjection for the given viewport and canvas box.

        Args:
            xy: Bottom-left canvas coordinate (x, y).
            width: Target box width on canvas (or None to derive from height).
            height: Target box height on canvas (or None to derive from width).
            lon_range: Longitude interval (min_lon, max_lon).
            lat_range: Latitude interval (min_lat, max_lat).
            scale: Proportional scale factor around xy.

        Returns:
            Configured GeoProjection instance.
        """
        if width is None and height is None:
            raise ValueError("At least one of 'width' or 'height' must be provided to GeoMap.draw().")

        min_lon, max_lon = float(lon_range[0]), float(lon_range[1])
        min_lat, max_lat = float(lat_range[0]), float(lat_range[1])
        if min_lon >= max_lon:
            raise ValueError(f"lon_range must have min_lon < max_lon, got {lon_range}.")
        if min_lat >= max_lat:
            raise ValueError(f"lat_range must have min_lat < max_lat, got {lat_range}.")

        lon_span = max_lon - min_lon
        lat_span = max_lat - min_lat
        mid_lat = (min_lat + max_lat) * 0.5
        # For global maps spanning >90 deg latitude, use a mild cosine factor; for regional maps, exact cos(mid_lat)
        eff_lat = min(65.0, abs(mid_lat)) if lat_span < 90.0 else 25.0
        cos_lat = math.cos(math.radians(eff_lat))
        natural_aspect = (lon_span * cos_lat) / lat_span

        bx, by = float(xy[0]), float(xy[1])
        if width is not None and height is not None:
            box_w = float(width)
            box_h = float(height)
            if box_w / box_h > natural_aspect:
                map_h = box_h
                map_w = box_h * natural_aspect
                map_x = bx + (box_w - map_w) * 0.5
                map_y = by
            else:
                map_w = box_w
                map_h = box_w / natural_aspect
                map_x = bx
                map_y = by + (box_h - map_h) * 0.5
        elif width is not None:
            box_w = float(width)
            box_h = box_w / natural_aspect
            map_x, map_y, map_w, map_h = bx, by, box_w, box_h
        elif height is not None:
            box_h = float(height)
            box_w = box_h * natural_aspect
            map_x, map_y, map_w, map_h = bx, by, box_w, box_h
        else:
            raise ValueError("At least one of 'width' or 'height' must be provided to GeoMap.draw().")

        return cls(
            min_lon=min_lon,
            min_lat=min_lat,
            max_lon=max_lon,
            max_lat=max_lat,
            cos_lat=cos_lat,
            box_x=bx,
            box_y=by,
            box_width=box_w,
            box_height=box_h,
            map_x=map_x,
            map_y=map_y,
            map_width=map_w,
            map_height=map_h,
            anchor_xy=(bx, by),
            scale=float(scale),
        )

    def project_unscaled(self, lon: float, lat: float) -> Point2D:
        """Project (lon, lat) into unscaled canvas coordinates (before canvas.transform scale)."""
        nx = (lon - self.min_lon) / (self.max_lon - self.min_lon)
        ny = (lat - self.min_lat) / (self.max_lat - self.min_lat)
        return (
            self.map_x + nx * self.map_width,
            self.map_y + ny * self.map_height,
        )

    def project_canvas(self, lon: float, lat: float) -> Point2D:
        """Project (lon, lat) into final canvas coordinates (accounting for scale around anchor_xy)."""
        ux, uy = self.project_unscaled(lon, lat)
        if self.scale == 1.0:
            return (ux, uy)
        ox, oy = self.anchor_xy
        return (
            ox + (ux - ox) * self.scale,
            oy + (uy - oy) * self.scale,
        )


__all__ = [
    "GeoProjection",
    "clip_ring_to_bbox",
]
