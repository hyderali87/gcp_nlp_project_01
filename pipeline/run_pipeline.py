from google.cloud import aiplatform

PROJECT_ID = "haks-genai"
REGION = "us-central1"  # ✅ match your failing region
BUCKET = "haks-bucket"

aiplatform.init(project=PROJECT_ID, location=REGION, staging_bucket=f"gs://{BUCKET}")

job = aiplatform.PipelineJob(
    display_name="nlp-translation-eval-run",
    template_path="translation_pipeline.json",
    pipeline_root=f"gs://{BUCKET}/pipelines",
    parameter_values={
        "gcs_csv_uri": f"gs://{BUCKET}/data/raw/sample_parallel.csv",
        "source_col": "source_text",
        "target_col": "target_text",
        "model_name": "Helsinki-NLP/opus-mt-en-hi",
        "output_gcs_uri": f"gs://{BUCKET}/outputs/translation_eval/run_002/"
    },
)

job.run()
print("Pipeline submitted.")

