FROM python:3.12 as prepare
WORKDIR /src
RUN pip install poetry
COPY pyproject.toml pyproject.toml
RUN poetry export -f requirements.txt --output requirements.txt

FROM python:3.6 as python36
WORKDIR /src
COPY --from=prepare /src/requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY test_lint.sh .pylintrc test_type.sh test_unit.sh drawlib /src/
RUN bash <<EOF
    ./test_lint.sh
    ./test_type.sh
    .test_unit.sh
EOF

