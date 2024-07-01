# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.


"""Validate function arguments data."""

from typing import Any, Dict, List, Optional

import drawlib.v0_2.private.validators.color as color_validator
import drawlib.v0_2.private.validators.coordinate as coordinate_validator
import drawlib.v0_2.private.validators.image as image_validator
import drawlib.v0_2.private.validators.line as line_validator
import drawlib.v0_2.private.validators.shape as shape_validator
import drawlib.v0_2.private.validators.smartarts as smartart_validator
import drawlib.v0_2.private.validators.style as style_validator
import drawlib.v0_2.private.validators.types as types_validator


def validate_canvas_args(args: Dict[str, Any]) -> None:  # noqa: C901
    """Validate configuration arguments.

    Args:
        args (Dict[str, Any]): Dictionary containing configuration arguments.

    Raises:
        ValueError: If any argument fails validation.

    """
    supported_formats = ["jpg", "png", "webp", "pdf"]

    for arg_name, value in args.items():
        if "self" == arg_name:
            continue

        if value is None:
            continue

        # config

        if "width" == arg_name:
            types_validator.validate_plus_float("width", value, is_0_ok=False)

        elif "height" == arg_name:
            types_validator.validate_plus_float("height", value, is_0_ok=False)

        elif "dpi" == arg_name:
            types_validator.validate_plus_int("dpi", value, is_0_ok=False)

        elif "theme" == arg_name:
            types_validator.validate_str("theme", value)

        elif "background_color" == arg_name:
            color_validator.validate_color("background_color", value)

        elif "background_alpha" == arg_name:
            types_validator.validate_plus_float("background_alpha", value)

        elif "grid" == arg_name:
            color_validator.validate_alpha("grid", value)

        elif "grid_only" == arg_name:
            types_validator.validate_bool("grid_only", value)

        elif "grid_style" == arg_name:
            style_validator.validate_linestyle("grid_style", value)

        elif "grid_centerstyle" == arg_name:
            style_validator.validate_linestyle("grid_style", value)

        elif "grid_xpitch" == arg_name:
            types_validator.validate_plus_float("grid_xpitch", value, is_0_ok=False)

        elif "grid_ypitch" == arg_name:
            types_validator.validate_plus_float("grid_ypitch", value, is_0_ok=False)

        # save

        elif "file" == arg_name:
            if value is not None:
                types_validator.validate_str("file", value)
                value = str(value).lower()
                ok = False
                for f in supported_formats:
                    if value.endswith(f):
                        ok = True
                        break
                if not ok:
                    raise ValueError(f"Save format supports only {supported_formats}.")

        elif "format" == arg_name:
            if value is not None:
                types_validator.validate_str("format", value)
                if value not in supported_formats:
                    raise ValueError(f'Save format supports only {supported_formats}. But "{value}" is provided.')

        else:
            raise ValueError(f'Drawlib internal bug. Argument "{arg_name}" is not validated at arg validator.')


def validate_icon_args(args: Dict[str, Any]) -> None:
    """Validate icon drawing arguments.

    Args:
        args (Dict[str, Any]): Dictionary containing icon drawing arguments.

    Raises:
        ValueError: If any argument fails validation.
    """
    for arg_name, value in args.items():
        if "self" == arg_name:
            continue

        # Check start from here

        if "xy" == arg_name:
            coordinate_validator.validate_xy("xy", value)

        elif "width" == arg_name:
            types_validator.validate_plus_float("width", value, is_0_ok=False)

        elif "angle" == arg_name:
            coordinate_validator.validate_angle("angle", value)

        elif "style" == arg_name:
            style_validator.validate_iconstyle("style", value)

        elif "code" == arg_name:
            types_validator.validate_str("code", value)

        elif "file" == arg_name:
            types_validator.validate_str("file", value)

        else:
            raise ValueError(f'Drawlib internal bug. Argument "{arg_name}" is not validated at arg validator.')


def validate_image_args(args: Dict[str, Any]) -> None:
    """Validate image drawing arguments.

    Args:
        args (Dict[str, Any]): Dictionary containing image drawing arguments.

    Raises:
        ValueError: If any argument fails validation.
    """
    for arg_name, value in args.items():
        if "self" == arg_name:
            continue

        # Check start from here

        if "xy" == arg_name:
            coordinate_validator.validate_xy("xy", value)

        elif "width" == arg_name:
            types_validator.validate_plus_float("width", value, is_0_ok=False)

        elif "image" == arg_name:
            image_validator.validate_image("image", value)

        elif "angle" == arg_name:
            coordinate_validator.validate_angle("angle", value)

        elif "style" == arg_name:
            style_validator.validate_imagestyle("style", value)

        else:
            raise ValueError(f'Drawlib internal bug. Argument "{arg_name}" is not validated at arg validator.')


def validate_line_args(args: Dict[str, Any]) -> None:  # noqa: C901
    """Validate line drawing arguments.

    Args:
        args (Dict[str, Any]): Dictionary containing line drawing arguments.

    Raises:
        ValueError: If any argument fails validation.
    """
    for arg_name, value in args.items():
        if "self" == arg_name:
            continue

        # Check start from here

        if "xy" == arg_name:
            coordinate_validator.validate_xy("xy", value)

        elif "xy1" == arg_name:
            coordinate_validator.validate_xy("xy1", value)

        elif "xy2" == arg_name:
            coordinate_validator.validate_xy("xy2", value)

        elif "xys" == arg_name:
            coordinate_validator.validate_xys("xys", value)

        elif "cp" == arg_name:
            coordinate_validator.validate_xy("cp", value)

        elif "cp1" == arg_name:
            coordinate_validator.validate_xy("cp1", value)

        elif "cp2" == arg_name:
            coordinate_validator.validate_xy("cp2", value)

        elif "path_points" == arg_name:
            coordinate_validator.validate_path_points("path_points", value)

        elif "width" == arg_name:
            if value is not None:
                types_validator.validate_plus_float("width", value, is_0_ok=False)

        elif "arrowhead" == arg_name:
            line_validator.validate_arrowhead("arrowhead", value)

        elif "bend" == arg_name:
            line_validator.validate_bend("bend", value)

        elif "r" == arg_name:
            types_validator.validate_plus_float("r", value)

        elif "style" == arg_name:
            style_validator.validate_linestyle("style", value)

        else:
            raise ValueError(f'Drawlib internal bug. Argument "{arg_name}" is not validated at arg validator.')


def validate_shape_args(  # noqa: C901
    args: Dict[str, Any],
    argnames_accept_none: Optional[List[str]] = None,
) -> None:
    """Validate shape drawing arguments.

    Args:
        args (Dict[str, Any]): Dictionary containing shape drawing arguments.
        argnames_accept_none (List[str], optional): List of argument names that can accept None as a value.

    Raises:
        ValueError: If any argument fails validation.
    """
    for arg_name, value in args.items():
        if argnames_accept_none is not None:
            if arg_name in argnames_accept_none:
                if value is None:
                    continue

        if "self" == arg_name:
            continue

        # Check start from here

        if "xy" == arg_name:
            coordinate_validator.validate_xy("xy", value)

        elif "xy1" == arg_name:
            coordinate_validator.validate_xy("xy1", value)

        elif "xy2" == arg_name:
            coordinate_validator.validate_xy("xy2", value)

        elif "xys" == arg_name:
            coordinate_validator.validate_xys("xys", value)

        elif "path_points" == arg_name:
            coordinate_validator.validate_path_points("path_points", value)

        elif "width" == arg_name:
            types_validator.validate_plus_float("width", value, is_0_ok=False)

        elif "height" == arg_name:
            types_validator.validate_plus_float("height", value, is_0_ok=False)

        elif "bottomedge_width" == arg_name:
            types_validator.validate_plus_float("bottomedge_width", value, is_0_ok=False)

        elif "topedge_width" == arg_name:
            types_validator.validate_plus_float("topedge_width", value, is_0_ok=False)

        elif "radius" == arg_name:
            types_validator.validate_plus_float("bottomedge_width", value, is_0_ok=False)

        elif "radius_ext" == arg_name:
            types_validator.validate_plus_float("bottomedge_width", value, is_0_ok=False)

        elif "radius_int" == arg_name:
            types_validator.validate_plus_float("bottomedge_width", value, is_0_ok=False)

        elif "num_vertex" == arg_name:
            shape_validator.validate_num_vertex("num_vertex", value)

        elif "topvertex_x" == arg_name:
            types_validator.validate_plusminus_float_or_none("topvertex_x", value)

        elif "topedge_x" == arg_name:
            types_validator.validate_plusminus_float_or_none("topvertex_x", value)

        elif "r" == arg_name:
            types_validator.validate_plus_float("r", value)

        elif "from_angle" == arg_name:
            coordinate_validator.validate_angle("from_angle", value)

        elif "to_angle" == arg_name:
            coordinate_validator.validate_angle("to_angle", value)

        elif "corner_angle" == arg_name:
            coordinate_validator.validate_angle_max90("corner_angle", value)

        elif "mirror" == arg_name:
            types_validator.validate_bool("mirror", value)

        elif "tail_width" == arg_name:
            types_validator.validate_plus_float("tail_width", value, is_0_ok=False)

        elif "head_width" == arg_name:
            types_validator.validate_plus_float("head_width", value, is_0_ok=False)

        elif "head_length" == arg_name:
            types_validator.validate_plus_float("head_length", value, is_0_ok=False)

        elif "head" == arg_name:
            shape_validator.validate_head_style("head", value)

        elif "is_default_center" == arg_name:
            types_validator.validate_bool("is_default_center", value)

        elif "text" == arg_name:
            types_validator.validate_str("text", value)

        elif "textsize" == arg_name:
            if value is not None:
                types_validator.validate_plus_float("textsize", value, is_0_ok=False)

        elif "angle" == arg_name:
            coordinate_validator.validate_angle("angle", value)

        elif "style" == arg_name:
            style_validator.validate_shapestyle("style", value)

        elif "textstyle" == arg_name:
            style_validator.validate_shapetextstyle("textstyle", value)

        #
        # smart art
        #

        elif "tail_edge" == arg_name:
            smartart_validator.validate_tail_edge("tail_edge", value)

        elif "tail_from_ratio" == arg_name:
            types_validator.validate_float_0_to_1("tail_from_ratio", value)

        elif "tail_vertex_xy" == arg_name:
            coordinate_validator.validate_xy("tail_vertex_xy", value)

        elif "tail_to_ratio" == arg_name:
            types_validator.validate_float_0_to_1("tail_to_ratio", value)

        else:
            raise ValueError(f'Drawlib internal bug. Argument "{arg_name}" is not validated at arg validator.')


def validate_text_args(args: Dict[str, Any]) -> None:
    """Validate text drawing arguments.

    Args:
        args (Dict[str, Any]): Dictionary containing text drawing arguments.

    Raises:
        ValueError: If any argument fails validation.
    """
    for arg_name, value in args.items():
        if "self" == arg_name:
            continue

        # Check start from here

        if "xy" == arg_name:
            coordinate_validator.validate_xy("xy", value)

        elif "text" == arg_name:
            types_validator.validate_str("text", value)

        elif "size" == arg_name:
            if value is not None:
                types_validator.validate_plus_float("size", value, is_0_ok=False)

        elif "angle" == arg_name:
            coordinate_validator.validate_angle("angle", value)

        elif "style" == arg_name:
            style_validator.validate_textstyle("style", value)

        else:
            raise ValueError(f'Drawlib internal bug. Argument "{arg_name}" is not validated at arg validator.')
