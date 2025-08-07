#!/bin/bash
curl -L https://huggingface.co/latincy/la_core_web_lg/resolve/main/la_core_web_lg-any-py3-none-any.whl -o la_core_web_lg-3.7.0-py3-none-any.whl && uv run pip install la_core_web_lg-3.7.0-py3-none-any.whl && rm la_core_web_lg-3.7.0-py3-none-any.whl
wget "https://zenodo.org/records/10473706/files/LIST_v1-2.parquet?download=1"
uv run python -c "import stanza; stanza.download('la')"
