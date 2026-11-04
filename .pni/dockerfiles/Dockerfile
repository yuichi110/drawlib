ARG PYTHON_VERSION=3.12
FROM ghcr.io/astral-sh/uv:python${PYTHON_VERSION}-bookworm-slim

ARG EXTRA_APT_PACKAGES=""
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy \
    VIRTUAL_ENV=/opt/pni-venv \
    PYTHONPATH="/workspace:/workspace/src" \
    PATH="/opt/pni-venv/bin:$PATH"

RUN if [ -n "${EXTRA_APT_PACKAGES}" ]; then \
      apt-get update \
      && apt-get install -y --no-install-recommends ${EXTRA_APT_PACKAGES} \
      && rm -rf /var/lib/apt/lists/*; \
    fi \
    && useradd --uid 10001 --create-home --shell /bin/bash pni \
    && mkdir -p /workspace /out /opt/pni-venv \
    && chown -R pni:pni /workspace /out /opt/pni-venv \
    && chmod 0777 /out

WORKDIR /workspace
COPY --chown=pni:pni . /workspace

RUN uv venv /opt/pni-venv \
    && if [ -f pyproject.toml ]; then \
         uv pip install --python /opt/pni-venv/bin/python -e . \
         || uv pip install --python /opt/pni-venv/bin/python .; \
       fi \
    && python3 -c 'import pathlib, subprocess, tomllib; p = pathlib.Path("pyproject.toml"); d = tomllib.loads(p.read_text(encoding="utf-8")) if p.is_file() else {}; groups = [x for v in d.get("dependency-groups", {}).values() if isinstance(v, list) for x in v if isinstance(x, str)]; opt = [x for v in d.get("project", {}).get("optional-dependencies", {}).values() if isinstance(v, list) for x in v if isinstance(x, str)]; deps = groups + opt; subprocess.run(["uv", "pip", "install", "--python", "/opt/pni-venv/bin/python", *deps], check=False) if deps else None' \
    && for req in requirements.txt requirements-dev.txt dev-requirements.txt; do \
         if [ -f "$req" ]; then uv pip install --python /opt/pni-venv/bin/python -r "$req"; fi; \
       done \
    && uv pip install --python /opt/pni-venv/bin/python pytest pytest-cov httpx uvicorn \
    && chown -R pni:pni /workspace /opt/pni-venv \
    && chmod -R a+rwX /workspace /opt/pni-venv

USER pni
CMD ["pytest"]
