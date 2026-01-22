#!/usr/bin/env bash
set -euo pipefail

: "${PROJECT_ID:?Need PROJECT_ID}"
: "${REGION:?Need REGION}"
: "${BUCKET:?Need BUCKET}"

echo "Running Vertex AI pipeline..."
cd pipeline

python run_pipeline.py
echo "Pipeline submitted."
