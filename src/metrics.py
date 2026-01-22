from __future__ import annotations
import sacrebleu

def compute_bleu_chrf(references: list[str], hypotheses: list[str]) -> dict:
    # sacrebleu expects: hypotheses list + list-of-reference-lists
    bleu = sacrebleu.corpus_bleu(hypotheses, [references]).score
    chrf = sacrebleu.corpus_chrf(hypotheses, [references]).score
    return {"bleu": float(bleu), "chrf": float(chrf)}



