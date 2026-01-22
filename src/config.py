from dataclasses import dataclass

@dataclass(frozen=True)
class Config:
    # Update these via pipeline parameters (preferred)
    source_col: str = "source_text"
    target_col: str = "target_text"

    # Baseline model (EN->HI). Replace for your language pair.
    # Examples:
    # EN->HI: Helsinki-NLP/opus-mt-en-hi
    # EN->TA: Helsinki-NLP/opus-mt-en-ta
    # EN->TE: Helsinki-NLP/opus-mt-en-te
    hf_model_name: str = "Helsinki-NLP/opus-mt-en-hi"

CFG = Config()

