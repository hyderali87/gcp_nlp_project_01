from __future__ import annotations
import pandas as pd
from transformers import pipeline

def translate_series(texts: list[str], model_name: str, batch_size: int = 8) -> list[str]:
    translator = pipeline("translation", model=model_name)
    outputs = translator(texts, batch_size=batch_size)
    return [o["translation_text"] for o in outputs]

def translate_dataframe(df: pd.DataFrame, source_col: str, model_name: str, batch_size: int = 8) -> pd.Series:
    preds = translate_series(df[source_col].tolist(), model_name=model_name, batch_size=batch_size)
    return pd.Series(preds)


