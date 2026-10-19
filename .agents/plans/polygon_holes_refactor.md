# Refactoring Plan: Add `holes` to `polygon()` and Migrate Icon Scripts

## 1. Goal & Scope
Add native interior cutout hole support (`holes` parameter) to `drawlib.shapes.polygon()`, and refactor all icon source scripts in `tools/icons_src/` to use `polygon(..., holes=...)` instead of the custom `draw_compound_polygon()` and `draw_layered_polygons()` helpers.

## 2. Core Library Changes (`src/drawlib/`)

### 2.1. Geometry & Path Helpers (`_core/l4_canvas/_shapes/_path_utils.py`)
- Add `signed_polygon_area(ring: list[Coordinate]) -> float` to compute signed 2D area (`> 0` for CCW, `< 0` for CW).
- Add `orient_polygon_ring(ring: list[Coordinate], *, ccw: bool) -> tuple[list[Coordinate], bool]` to return a copy of `ring` oriented CCW (`ccw=True`) or CW (`ccw=False`), plus a boolean indicating whether the vertex order was reversed.
- Export both helpers in `_path_utils.py` and re-export on `ShapeUtils` in `_shape_utils.py`.

### 2.2. Public `polygon()` Method (`_core/l4_canvas/_shapes/_polygon.py`)
- Update signature:
  ```python
  @validate_call
  def polygon(
      self,
      xys: Coordinates,
      *,
      holes: list[Coordinates] | None = None,
      style: Style,
      text: str = "",
      text_style: Style | None = None,
  ) -> None:
  ```
- **Validation**:
  - Require `len(xys) >= 3` (`ValueError` otherwise).
  - For each `hole` in `holes` (when `holes` is non-empty), require `len(hole) >= 3` (`ValueError` otherwise).
- **Rendering without `holes`** (`not holes`):
  - Keep existing behavior unchanged (`Polygon` patch when unrounded, `PathPatch` when rounded via `style.shape_r`).
- **Rendering with `holes`**:
  - Orient outer `xys` counter-clockwise (`ccw=True`). If reversed and `style.shape_r` is a tuple, reverse the `shape_r` tuple so per-vertex radii stay paired with their original vertices.
  - Round outer vertices via `ShapeUtils.round_polygon_points(outer_pts, outer_shape_r)` and build `outer_path = ShapeUtils.build_matplotlib_path(...)`.
  - For each `hole` in `holes`, orient clockwise (`ccw=False`). If `style.shape_r` is a scalar `float`, apply `round_polygon_points(hole_pts, style.shape_r)`; if `style.shape_r` is a tuple (which belongs to `xys`), leave hole corners unrounded. Build `hole_path = ShapeUtils.build_matplotlib_path(...)`.
  - Combine subpaths via `Path.make_compound_path(outer_path, *hole_paths)` and append `PathPatch(path=compound_path, **options)` to `self._artists`.
- **Text anchor**: Keep embedded `text` centered on the outer `xys` bounding box (`get_center_and_size(xys)`).

### 2.3. Docstrings, Rules & Official Docs
- Update `polygon()` docstring following `@validate_call` docstring rules (no internal type aliases).
- Update `src/drawlib/_rules/lib_shapes.md` and `src/drawlib/_rules/api.md` to document `holes`.
- Update `docs/docs_src/02_drawing_primitives/shapes_polygon.md` parameter table and example to demonstrate `holes`.

## 3. Icon Source Migration (`tools/icons_src/`)
- Replace all 844 uses of `draw_compound_polygon()` and 330 uses of `draw_layered_polygons()` (1,174 scripts total) with `polygon(..., holes=..., style=fill_style(...))`.
- Decompose multi-contour ring lists by containment depth (`depth % 2 == 0` as outer contour, direct `depth + 1` children as `holes`).
- Preserve variable references (`whale_body`, `ring_outer`, `c1[0]`, etc.) in scripts that pass named variables instead of inline literals.
- For `tools/icons_src/code/deno_default.py` (the single `draw_layered_polygons` script without a background plate), draw the white circle base first and then draw the black `polygon(..., holes=...)` on top.
- Remove `draw_compound_polygon()`, `draw_layered_polygons()`, `_splice_holes_into_outer()`, `_signed_area()`, `_point_in_ring()`, `_orient_ring()`, and `_ring_inside_ring()` from `tools/icons_src/utils.py`.

## 4. Verification & Testing
1. Add unit tests for `polygon(..., holes=...)` in `tests/drawlib/_core/l4_canvas/test_polygon.py` (single hole, multiple holes, CW/CCW auto-orientation, `shape_r` scalar and tuple with holes, `canvas.transform` with holes, and `< 3` vertex validation errors).
2. Run `./dcli test target core` and `./dcli test target icons`.
3. Rebuild all icons via `./tools/icons_src/build.sh` and sync release asset hashes via `./dcli release-assets sync`.
4. Visually inspect representative re-rendered icons and updated documentation images via `view_file`.
5. Run `./dcli code-check all` and `./dcli docs build site --no-clean` + `./dcli docs serve site --check`.
