from dataclasses import dataclass
from typing import List, Dict, Optional
import re
import pandas as pd
from rapidfuzz import process, fuzz
import chromadb 
from chromadb.utils import embedding_functions

'''
Implemented exact match and fuzzy match 
'''

FUZZY_ACCEPT = 85.0
FUZZY_GAP = 6.0
TOPK = 4

SEMANTIC_DISTANCE = 0.35  
SEMANTIC_GAP = 0.05

def normalize(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"[\s\-_]+", " ", s)
    s = re.sub(r"[^\w\s]", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


@dataclass
class Candidate:
    product_id: str
    product_name: str
    score: float


@dataclass
class ResolveResult:
    resolved_product_id: Optional[str]
    resolved_product_name: Optional[str]
    resolution_method: str          # {exact | fuzzy | semantic | none }
    resolution_confidence: float    # capped from 0 to 1 
    candidates: Optional[List[Candidate]]
    failure_reason: Optional[str] = None  # {ambiguous | below_threshold | no_match}


class ProductResolver:
    def __init__(self, 
                 product_table: Optional[pd.DataFrame] = None,
                 chroma_path: str = "chroma_store",
                 chroma_collection: str = "Semantic_Embeddings"):
        if product_table is None:
            self.table = pd.read_parquet("Data/Final_Table.parquet")
        else:
            self.table = product_table

        self.id_dict: Dict[str, Dict[str, str]] = {}
        self.norm_dict: Dict[str, List[Dict[str, str]]] = {}
        self.fuzzy_choices: List[str] = []
        
        for _,row in self.table.iterrows():
            pid = str(row.get("product_id", ""))
            pname = str(row.get("product_name", ""))
            norm = str(row.get("norm_name", ""))

            self.id_dict[pid] = {"product_id": pid ,"product_name" : pname} 
            row_obj = {"product_id": pid, "product_name": pname, "norm_name": norm}
            if norm not in self.norm_dict:
                self.norm_dict[norm] = []
                self.fuzzy_choices.append(norm)  

            self.norm_dict[norm].append(row_obj)

        self.client = chromadb.PersistentClient(path = chroma_path)
        self.emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="jinaai/jina-embeddings-v2-base-en",trust_remote_code=True)
        self.collection = self.client.get_or_create_collection(
            name = chroma_collection,
            embedding_function = self.emb_fn
        )


    def resolve(self, query: str) -> ResolveResult:
        q_raw = (query or "").strip()
        if not q_raw:
            return ResolveResult(None, None, "none", 0.0, [], "no_match")

        q_norm = normalize(q_raw)

        # 1) exact by product_id
        if q_raw in self.id_dict:
            row = self.id_dict[q_raw]
            return ResolveResult(row["product_id"], row["product_name"], "exact", 1.0, None)

        # 2) exact by normalized name
        norm_name_rows = self.norm_dict.get(q_norm)
        if norm_name_rows :
            if len(norm_name_rows) == 1:
                r = norm_name_rows[0] 
                return ResolveResult(r["product_id"], r["product_name"], "exact", 1.0, None)
            else:
                cands = [Candidate(r["product_id"], r["product_name"], 100.0) for r in norm_name_rows[:TOPK]]
                return ResolveResult(None, None, "none", 0.0, cands, "ambiguous")           

        # 3) fuzzy by normalized name
        matches = process.extract(q_norm, self.fuzzy_choices, scorer=fuzz.token_set_ratio, limit=TOPK)

        fuzzy_candidates = []
        for match_norm, score, _ in matches:
            rows = self.norm_dict.get(match_norm, [])
            for r in rows:
                fuzzy_candidates.append(Candidate(r["product_id"], r["product_name"], float(score)))

        fuzzy_candidates.sort(key = lambda x: x.score ,reverse=True)
        fuzzy_candidates = fuzzy_candidates[:TOPK]

        if fuzzy_candidates:
            top1 = fuzzy_candidates[0]
            top2 = fuzzy_candidates[1] if len(fuzzy_candidates) > 1 else None

            gap_ok = True  if (top2 is None) else ((top1.score - top2.score) >= FUZZY_GAP)
            
            if top1.score >= FUZZY_ACCEPT and gap_ok:
                conf = min(0.95, top1.score / 100.0)
                return ResolveResult(top1.product_id, top1.product_name, "fuzzy", conf, fuzzy_candidates)
                
        results = self.collection.query(
            query_texts=[q_norm], 
            n_results=2 
        )
        
        
        if not results['ids'] or not results['ids'][0]:
            return ResolveResult(None, None, "none", 0.0, fuzzy_candidates, "no_match")
        
        if not results['distances'] or not results['distances'][0]:
            return ResolveResult(None, None, "none", 0.0, fuzzy_candidates, "no_distance")
        
        ids = results.get('ids',[])
        distances = results.get('distances',[])

        top_id = ids[0][0]
        top_dist = distances[0][0]

        second_dist = distances[0][1] if len(distances[0]) > 1 else 1.0

        if top_dist is None:
            return ResolveResult(None, None, "none", 0.0, fuzzy_candidates, "no_distance")
        
        sem_gap_ok = True if (second_dist is None) else ((second_dist - top_dist) >= SEMANTIC_GAP)
        sem_dist_ok = top_dist <= SEMANTIC_DISTANCE

        if sem_dist_ok and sem_gap_ok and (top_id in self.id_dict):
            res = self.id_dict[top_id]
            conf = max(0.0, min(1.0, 1.0 - float(top_dist)))
            return ResolveResult(res["product_id"], res["product_name"], "semantic", conf, [])

        reason = "below_threshold" if not sem_dist_ok else "ambiguous"
        return ResolveResult(None, None, "none", 0.0, fuzzy_candidates, f"semantic_{reason}")

