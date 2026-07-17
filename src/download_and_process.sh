#!/bin/bash
echo "going to download TEIs from Transkribus from ${TR_DL_URL}"
wget -O out.zip ${TR_DL_URL}
rm -rf tmp && mkdir tmp
unzip -o out.zip -d tmp
uv run src/make_teis.py
