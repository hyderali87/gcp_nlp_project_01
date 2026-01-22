#!/usr/bin/env bash
set -euo pipefail

echo "Compiling KFP pipeline..."
cd pipeline
python compile.py
ls -lh translation_pipeline.json
echo "Compile done."
