# GCP MLOps NLP Translation (Vertex AI Pipelines)

This project runs a simple translation pipeline on GCP using:
- Vertex AI Pipelines (KFP v2)
- Artifact Registry (Docker image)
- GCS (dataset + pipeline artifacts)
- Hugging Face translation model (baseline)
- Metrics: BLEU and chrF

## Prerequisites
- GCP Project
- APIs enabled: Vertex AI, Artifact Registry, Cloud Build, GCS
- A GCS bucket for data/artifacts
- A parallel CSV in GCS with columns: source_text,target_text

## Quick steps (Cloud Shell)
1) Set env:
   export PROJECT_ID="haks-genai"
   export REGION="us-central1"
   export BUCKET="haks-bucket"

2) Build + push image:
   gcloud services enable aiplatform.googleapis.com artifactregistry.googleapis.com cloudbuild.googleapis.com storage.googleapis.com
   gcloud artifacts repositories create mlops-repo --repository-format=docker --location=$REGION || true
   gcloud auth configure-docker $REGION-docker.pkg.dev
   docker build -t $REGION-docker.pkg.dev/$PROJECT_ID/mlops-repo/nlp-translation:latest .
   docker push $REGION-docker.pkg.dev/$PROJECT_ID/mlops-repo/nlp-translation:latest

3) Compile pipeline:
   cd pipeline
   python compile.py

4) Run pipeline:
   python run_pipeline.py

Monitor:
- Vertex AI -> Pipelines
