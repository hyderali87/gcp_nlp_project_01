from kfp import compiler
from pipeline import pipeline

compiler.Compiler().compile(
    pipeline_func=pipeline,
    package_path="translation_pipeline.json"
)

print("Compiled: translation_pipeline.json")
