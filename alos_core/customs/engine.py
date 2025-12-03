# alos_core/customs/engine.py
from typing import List, Dict, Any

import torch
from sentence_transformers import SentenceTransformer, util

from .normalizer import ArmNormalizer


class CustomsEngine:
    """
    Мини-MVP движка:
    - нормализация армянского/смешанного текста
    - эмбеддинги через sentence-transformers
    - поиск ближайшего описания в маленькой базе
    """

    def __init__(self, model_name: str = "paraphrase-multilingual-MiniLM-L12-v2"):
        self.model = SentenceTransformer(model_name)
        self.normalizer = ArmNormalizer()

        # MVP knowledge base – 4–5 позиций
        # TODO: вынести в отдельный references.py + БД
        self.knowledge_base: List[Dict[str, Any]] = [
            {
                "desc": "wireless bluetooth speaker portable audio device",
                "hs_code": "851821",
                "risk": "low",
            },
            {
                "desc": "smartphone mobile phone iphone samsung with encryption",
                "hs_code": "851712",
                "risk": "encryption",
            },
            {
                "desc": "electric drill power tool for construction",
                "hs_code": "846721",
                "risk": "dual-use",
            },
            {
                "desc": "cotton t-shirt men clothing",
                "hs_code": "610910",
                "risk": "low",
            },
        ]

        self.kb_vectors = self.model.encode(
            [k["desc"] for k in self.knowledge_base], convert_to_tensor=True
        )

    def predict_hs(self, raw_query: str) -> Dict[str, Any]:
        normalized = self.normalizer.normalize(raw_query)
        if not normalized:
            return {
                "raw_input": raw_query,
                "normalized": normalized,
                "matched_desc": None,
                "confidence": 0.0,
                "hs_code": None,
                "risk_flag": None,
            }

        query_emb = self.model.encode(normalized, convert_to_tensor=True)
        cos_scores = util.cos_sim(query_emb, self.kb_vectors)[0]
        topk = torch.topk(cos_scores, k=1)

        score = float(topk.values[0].item())
        idx = int(topk.indices[0].item())
        match = self.knowledge_base[idx]

        return {
            "raw_input": raw_query,
            "normalized": normalized,
            "matched_desc": match["desc"],
            "confidence": round(score, 3),
            "hs_code": match["hs_code"],
            "risk_flag": match["risk"],
        }


if __name__ == "__main__":
    engine = CustomsEngine()
    samples = ["բլուտուզ խոսփաքեր", "айфон 15 про", "электро дрель", "мужская футболка хлопок"]

    for s in samples:
        res = engine.predict_hs(s)
        print(f"{s!r} -> HS {res['hs_code']} ({res['confidence']}) [{res['matched_desc']}]")
