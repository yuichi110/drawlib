# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

# ruff: noqa: S102, PLC0415

"""Image utility functions."""

from __future__ import annotations

import io
import multiprocessing as mp
import multiprocessing.connection
from typing import Any

from PIL import Image

from drawlib._core.l1_core import guarded
from drawlib._core.l2_models import Dimage


def _worker_render_code(
    code: str,
    conn: multiprocessing.connection.Connection,
) -> None:
    """Worker function executed in an isolated child process.

    Args:
        code (str): Drawlib code block to execute.
        conn (multiprocessing.connection.Connection): IPC pipe connection endpoint.
    """
    try:
        import drawlib._core.l4_canvas._canvas
        import drawlib.canvas

        # Reset canvas to a clean state in the worker process (clearing any inherited state from fork)
        drawlib.canvas.clear()

        # Intercept save() to be a no-op before user code executes
        def _no_op_save(*args: Any, **kwargs: Any) -> None:  # noqa: ANN401
            pass

        drawlib.canvas.save = _no_op_save
        drawlib._core.l4_canvas._canvas.save = _no_op_save
        drawlib._core.l4_canvas._canvas.canvas.save = _no_op_save

        exec_globals: dict[str, Any] = {
            "__name__": "__main__",
            "save": _no_op_save,
        }

        compiled = compile(code, filename="<dimage_code>", mode="exec")
        exec(compiled, exec_globals)

        dimg = drawlib.canvas.get_dimage()
        pil_img = dimg.get_pil_image()
        bio = io.BytesIO()
        pil_img.save(bio, format="PNG")
        conn.send((True, bio.getvalue()))
    except Exception as e:
        conn.send((False, f"{type(e).__name__}: {e}"))
    finally:
        conn.close()


@guarded
def get_dimage_from_code(
    code: str,
    timeout: float | None = None,
) -> Dimage:
    """Render drawlib code in an isolated subprocess and return the result as a Dimage.

    This function executes the provided drawlib drawing code in an isolated child process,
    ignoring any save() calls inside the code, and captures the rendered canvas as a Dimage.
    Because execution happens in a separate process, the parent process's canvas state,
    preset styles, and matplotlib global settings remain completely unaffected.

    Args:
        code (str): Drawlib Python drawing code snippet.
        timeout (float | None, optional): Maximum execution time in seconds. Defaults to None.

    Returns:
        Dimage: The rendered canvas image.

    Raises:
        RuntimeError: If code execution fails or the process terminates unexpectedly.
        TimeoutError: If execution exceeds the specified timeout.
    """
    parent_conn, child_conn = mp.Pipe()
    process = mp.Process(target=_worker_render_code, args=(code, child_conn))
    process.start()
    child_conn.close()

    try:
        if timeout is not None:
            if parent_conn.poll(timeout=timeout):
                success, data = parent_conn.recv()
            else:
                process.kill()
                raise TimeoutError(f"Rendering Dimage from code timed out after {timeout} seconds.")
        else:
            success, data = parent_conn.recv()
    except EOFError as err:
        raise RuntimeError("Worker process terminated unexpectedly while rendering Dimage.") from err
    finally:
        process.join()
        parent_conn.close()

    if not success:
        raise RuntimeError(f"Error executing drawlib code for Dimage: {data}")

    image_buffer = io.BytesIO(data)
    pil_image = Image.open(image_buffer)
    pil_image.load()
    return Dimage(pil_image)
