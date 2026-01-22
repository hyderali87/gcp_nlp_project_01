from kfp import dsl

@dsl.component
def translation_eval_component(
    gcs_csv_uri: str,
    source_col: str,
    target_col: str,
    model_name: str,
    output_gcs_uri: str,
):
    """
    Downloads parallel CSV from GCS, runs batch translation, computes BLEU & chrF,
    and writes predictions + metrics to GCS.
    """
    import json
    import os
    import pandas as pd
    from google.cloud import storage

    from src.data_prep import load_parallel_csv
    from src.translate_batch import translate_dataframe
    from src.metrics import compute_bleu_chrf

    def gcs_to_local(gcs_uri: str, local_path: str):
        if not gcs_uri.startswith("gs://"):
            raise ValueError(f"Expected gs:// URI, got: {gcs_uri}")
        parts = gcs_uri.replace("gs://", "").split("/", 1)
        bucket_name = parts[0]
        blob_name = parts[1] if len(parts) > 1 else ""
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.download_to_filename(local_path)

    def local_to_gcs(local_path: str, gcs_uri: str):
        parts = gcs_uri.replace("gs://", "").split("/", 1)
        bucket_name = parts[0]
        blob_name = parts[1] if len(parts) > 1 else ""
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.upload_from_filename(local_path)

    # 1) Download data
    local_csv = "/tmp/parallel.csv"
    gcs_to_local(gcs_csv_uri, local_csv)

    # 2) Prep
    df = load_parallel_csv(local_csv, source_col, target_col)

    # 3) Translate
    df["prediction"] = translate_dataframe(df, source_col, model_name=model_name, batch_size=8)

    # 4) Metrics
    metrics = compute_bleu_chrf(
        references=df[target_col].tolist(),
        hypotheses=df["prediction"].tolist()
    )

    print("METRICS:", metrics)

    # 5) Save outputs locally
    pred_path = "/tmp/predictions.csv"
    df.to_csv(pred_path, index=False)

    metrics_path = "/tmp/metrics.json"
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, ensure_ascii=False, indent=2)

    # 6) Upload to GCS
    # output_gcs_uri is a folder-like prefix, we write two objects under it
    if not output_gcs_uri.endswith("/"):
        output_gcs_uri += "/"

    local_to_gcs(pred_path, output_gcs_uri + "predictions.csv")
    local_to_gcs(metrics_path, output_gcs_uri + "metrics.json")


@dsl.pipeline(
    name="nlp-translation-eval-pipeline",
    pipeline_root="gs://YOUR_BUCKET/pipelines"  # replace before compile
)
def pipeline(
    gcs_csv_uri: str = "gs://YOUR_BUCKET/data/raw/sample_parallel.csv",
    source_col: str = "source_text",
    target_col: str = "target_text",
    model_name: str = "Helsinki-NLP/opus-mt-en-hi",
    output_gcs_uri: str = "gs://YOUR_BUCKET/outputs/translation_eval/run_001/",
):
    translation_eval_component(
        gcs_csv_uri=gcs_csv_uri,
        source_col=source_col,
        target_col=target_col,
        model_name=model_name,
        output_gcs_uri=output_gcs_uri,
    )
