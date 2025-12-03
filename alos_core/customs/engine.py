# alos_core/customs/engine.py
from typing import List, Dict, Any

import torch
from sentence_transformers import SentenceTransformer, util

from .normalizer import ArmNormalizer


class CustomsEngine:
    """
    Mini-MVP customs engine for ALOS ANI (Automated Neural Inspector).

    Pipeline:
    - normalize raw text (Armenian / Russian / mixed) into a cleaner form
    - encode it with a multilingual SentenceTransformer
    - semantic search over a tiny in-memory knowledge base
    - return HS code, risk flag and confidence
    """

    def __init__(self, model_name: str = "paraphrase-multilingual-MiniLM-L12-v2"):
        # multilingual model, works with 50+ languages
        self.model = SentenceTransformer(model_name)
        self.normalizer = ArmNormalizer()

        # MVP knowledge base – just a few reference descriptions
        # In a real system this would live in a proper DB / vector store.
        self.knowledge_base: List[Dict[str, Any]] = [
            {
                # added Armenian/Russian slang so "blutuz khospaker" lands here
                "desc": (
                    "wireless bluetooth speaker portable audio device "
                    "blutuz khospaker колонка blutuz speaker"
                ),
                "hs_code": "851821",
                "risk": "low",
            },
            {
                "desc": (
                    "smartphone mobile phone iphone samsung айфон телефон "
                    "smart phone"
                ),
                "hs_code": "851712",
                "risk": "encryption",
            },
            {
                "desc": (
                    "electric drill power tool for construction "
                    "электро дрель дрель instrument"
                ),
                "hs_code": "846721",
                "risk": "dual-use",
            },
            {
                "desc": (
                    "cotton t-shirt men clothing мужская футболка хлопок "
                    "apparel textile"
                ),
                "hs_code": "610910",
                "risk": "low",
            },
        ]

        # Pre-encode KB descriptions into vectors once
        self.kb_vectors = self.model.encode(
            [k["desc"] for k in self.knowledge_base],
            convert_to_tensor=True,
        )

    def predict_hs(self, raw_query: str) -> Dict[str, Any]:
        """
        Take raw invoice/description string and return:
        - normalized text
        - best matching KB description
        - cosine similarity (confidence)
        - HS code
        - simple risk flag
        - human_review: whether a human should double-check
        """
        normalized = self.normalizer.normalize(raw_query)

        if not normalized:
            return {
                "raw_input": raw_query,
                "normalized": normalized,
                "matched_desc": None,
                "confidence": 0.0,
                "hs_code": None,
                "risk_flag": None,
                "human_review": True,
            }

        # Encode query
        query_emb = self.model.encode(normalized, convert_to_tensor=True)

        # Semantic search: cosine similarity vs all KB vectors
        cos_scores = util.cos_sim(query_emb, self.kb_vectors)[0]
        topk = torch.topk(cos_scores, k=1)

        score = float(topk.values[0].item())
        idx = int(topk.indices[0].item())
        match = self.knowledge_base[idx]

        # simple threshold for human-in-the-loop
        human_review = score < 0.6

        return {
            "raw_input": raw_query,
            "normalized": normalized,
            "matched_desc": match["desc"],
            "confidence": round(score, 3),
            "hs_code": match["hs_code"],
            "risk_flag": match["risk"],
            "human_review": human_review,
        }


if __name__ == "__main__":
    engine = CustomsEngine()
    samples = [
        "բլուտուզ խոսփաքեր",
        "айфон 15 про",
        "электро дрель",
        "мужская футболка хлопок",
        "bluetooth speaker",
        "дрель power tool",
    ]

    for s in samples:
        res = engine.predict_hs(s)
        print(
            f"{s!r} -> HS {res['hs_code']} "
            f"(conf={res['confidence']}) "
            f"[match='{res['matched_desc']}'] "
            f"norm='{res['normalized']}' "
            f"human_review={res['human_review']}"
        )
