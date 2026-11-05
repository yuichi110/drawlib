ARG PYTHON_VERSION=3.12
FROM ghcr.io/astral-sh/uv:python${PYTHON_VERSION}-bookworm-slim

ARG EXTRA_APT_PACKAGES=""
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy \
    VIRTUAL_ENV=/opt/pni-venv \
    PLAYWRIGHT_BROWSERS_PATH=/opt/ms-playwright \
    PYTHONPATH="/workspace:/workspace/src" \
    PATH="/opt/pni-venv/bin:$PATH"

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       libgl1 \
       libglx-mesa0 \
       libglib2.0-0 \
       ${EXTRA_APT_PACKAGES} \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --uid 10001 --create-home --shell /bin/bash pni \
    && mkdir -p /workspace /out /opt/pni-venv /opt/ms-playwright \
    && chown -R pni:pni /workspace /out /opt/pni-venv /opt/ms-playwright \
    && chmod 0777 /out

WORKDIR /workspace
COPY --chown=pni:pni pyproject.toml ./
COPY --chown=pni:pni docs_src/README_PYPI.md ./docs_src/README_PYPI.md
COPY --chown=pni:pni docs_src/api/ ./docs_src/api/
COPY --chown=pni:pni src/ ./src/

# Install drawlib in editable mode with baseline rendering versions matching test answer PNGs
RUN uv venv /opt/pni-venv \
    && uv pip install --python /opt/pni-venv/bin/python -e . \
    && uv pip install --python /opt/pni-venv/bin/python \
       pytest \
       pytest-cov \
       pytest-xdist \
       tomlkit \
       matplotlib==3.10.9 \
       "pillow>=13.0.0"

# Pre-install headless Chromium OS libs & shell plus drawlib font/icon caches for --network=none tests
RUN playwright install-deps chromium \
    && rm -rf /var/lib/apt/lists/* \
    && playwright install --only-shell chromium \
    && drawlib cache download --all

COPY --chown=pni:pni tests/ ./tests/
RUN mkdir -p /workspace/output_tests \
    && chown -R pni:pni /workspace /opt/pni-venv /opt/ms-playwright \
    && chmod -R a+rwX /workspace /opt/pni-venv /opt/ms-playwright

USER pni
CMD ["pytest"]
