import pandas as pd
import re
from resolver import ProductResolver
import json
import ollama
from rapidfuzz import fuzz
import chromadb 
from chromadb.utils import embedding_functions


SOP_CONFIG = {
    "Basic Information": {
        "sop_id": "SOP-01",
        "required_fields": ["product_name", "department_name", "aisle_name"],
        "critical_fields": ["product_name", "department_name", "aisle_name"],
        "failure_code": "MISSING_DATA",
    },
    "Detailed Information": {
        "sop_id": "SOP-02",
        "required_fields": [
            "product_name",
            "department_name",
            "aisle_name",
            "total_orders",
            "popularity_segment",
            "popularity_rank",
            "reorder_rate",
            "repeat_user_count",
            "orders_per_users",
            "dominant_day",
            "dominant_hour",
            "early_week_percent",
            "mid_week_percent",
            "weekend_percent",
            "morning_percent",
            "afternoon_percent",
            "evening_percent",
            "night_percent",
            "avg_cart_position",
            "cart_position_segment",
            "bought_together_names",
            "counts_of_bought_together",
        ],
        "critical_fields": ["product_name", "department_name", "aisle_name"],
        "failure_code": "INSUFFICIENT_PRODUCT_PROFILE",
    },
    "Similar Products": {
        "sop_id": "SOP-03",
        "required_fields": ["product_name", "department_name", "aisle_name"],
        "critical_fields": ["product_name", "department_name", "aisle_name"],
        "failure_code": "NO_VALID_SIMILAR_PRODUCTS",
    },
    "Bought Together": {
        "sop_id": "SOP-04",
        "required_fields": ["bought_together_names", "counts_of_bought_together"],
        "critical_fields": ["bought_together_names","product_name", "department_name", "aisle_name"],
        "failure_code": "NO_CO_PURCHASE_DATA",
    },
    "Product Comparison": {
        "sop_id": "SOP-05",
        "required_fields": [
            "product_name",
            "department_name",
            "aisle_name",
            "total_orders",
            "popularity_segment",
            "popularity_rank",
            "reorder_rate",
            "repeat_user_count",
            "orders_per_users",
            "dominant_day",
            "dominant_hour",
            "early_week_percent",
            "mid_week_percent",
            "weekend_percent",
            "morning_percent",
            "afternoon_percent",
            "evening_percent",
            "night_percent",
            "avg_cart_position",
            "cart_position_segment",
        ],
        "critical_fields": ["product_name", "department_name", "aisle_name"],
        "failure_code": "COMPARISON_NOT_POSSIBLE",
    },
    "Product Popularity": {
        "sop_id": "SOP-06",
        "required_fields": ["total_orders", "popularity_segment", "popularity_rank", "reorder_rate"],
        "critical_fields": ["total_orders", "popularity_segment","product_name", "department_name", "aisle_name"],
        "failure_code": "NO_POPULARITY_DATA",
    },
    "Shopping Behavior": {
        "sop_id": "SOP-07",
        "required_fields": [
            "product_name",
            "department_name",
            "aisle_name",
            "total_orders",
            "popularity_bucket",
            "unique_users",
            "reorder_rate",
            "orders_per_users",
            "avg_cart_position",
            "cart_position_segment",
        ],
        "critical_fields": ["product_name", "department_name", "aisle_name"],
        "failure_code": "NO_SHOPPING_BEHAVIOR_DATA",
    },
}

direct_intent = {
    "Detailed Information" : ["more details", "tell me everything", "full details", "describe it properly", "give complete info","everything", "detailed profile"],
    "Similar Products" : ["similar products", "products like this", "alternatives", "similar items", "products similar to this"],
    "Bought Together" : ["bought together", "frequently bought together", "often bought with this", "commonly bought together", "products bought together","usually purchased along with","paired with"],
    "Product Comparison" : ["compare with", "comparison", "compare to", "how does it compare", "comparison with", "compare this with", "vs", "versus", "difference between","better than", "worse than"],
    "Product Popularity" : ["popularity", "how popular", "popularity of this product", "is it popular", "popularity ranking", "how well it sells", "high demand", "trending"],
    "Shopping Behavior" : ["shopping behavior", "customer behavior", "how do people shop for this", "customer shopping behavior", "how customers buy this", "shopping patterns for this" ,"reorder" ,"frequency of purchase" ,"repurchase rate", "how often", "unique users", "buyers"] 
}

def normalize(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"[\s\-_]+", " ", s)
    s = re.sub(r"[^\w\s]", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

FUZZY_ACCEPT = 85.0
FUZZY_GAP = 6.0

def intent(query):
    query_norm = normalize(query.lower())

    for intent, phrases in direct_intent.items():
        for phrase in phrases:
            if normalize(phrase) in query_norm:
                return intent


    #fuzzy 
    best_intent  = None
    best_score = 0
    second_best_score = 0

    for intent, phrases in direct_intent.items():
        current_best = 0
        for phrase in phrases:
            s = fuzz.partial_ratio(query_norm, phrase)
            if s > current_best:
                current_best = s
        
        if(current_best > best_score):
            second_best_score = best_score
            best_score = current_best
            best_intent = intent
        elif current_best > second_best_score:
            second_best_score = current_best

    gap = best_score - (second_best_score if second_best_score >= 0 else 0)

    if best_intent is not None and best_score >= FUZZY_ACCEPT and gap >= FUZZY_GAP:
        return best_intent

    ollama_response = ollama.chat(
        model = "mistral:latest",
        messages = [
            {
                "role" : "system",
                "content" : "You are intent classifier which must return JSON object with keys : intent and confidence"
                "Intent can only be one of :"
                "Detailed Information, Similar Products, Bought Together, Product Comparison, Product popularity, Shopping Behavior"
                "Confidence must be from 0 to 1 only "
                "If unsure return Basic Information with low confidence"
            },
            {
                "role" : "user",
                "content" : f"Classify the intent of following {query_norm}"
            }
        ]
    )

    raw = ollama_response["message"]["content"]
    try:
        obj = json.loads(raw)
        intent_label = obj.get("intent", "Basic Information")
        return intent_label if intent_label in SOP_CONFIG else "Basic Information"
    except Exception:
        return "Basic Information"


class ProductRouter:
    def __init__(self,path="chroma_store"):
        self.resolver = ProductResolver()

        self.client = chromadb.PersistentClient(path=path)
        self.emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="jinaai/jina-embeddings-v2-base-en")
        self.collection_sops = self.client.get_or_create_collection(name = "SOPs_Embeddings",embedding_function = self.emb_fn)
    
    def get_product_data(self, product_id, fields):
        row = self.resolver.table[self.resolver.table['product_id'] == product_id]

        if row.empty:
            return None
        
        existing_fields = [f for f in fields if f in row.columns]
        if not existing_fields:
            return None
        
        return row[existing_fields].to_dict(orient='records')[0]
    
    def sop_call(self,query,result):
        query_intent = intent(query)
        sop_id = SOP_CONFIG.get(query_intent)
        if sop_id is None: 
            return self.failure_response(query, result, meta={"reason": "unknown_intent_label", "query_intent": query_intent})
        
        fields = list(dict.fromkeys(sop_id["required_fields"] + sop_id["critical_fields"]))
        product_data = self.get_product_data(result.resolved_product_id,fields)

        if product_data is None :
            return self.failure_response(query, result, meta={"reason": "no_product_data_available"})
        
        critical_field = sop_id["critical_fields"]
        missing_critical = []
        for field in critical_field:
            val = product_data.get(field)
            if val is None or (isinstance(val, float) and pd.isna(val)) or pd.isna(val):
                missing_critical.append(field)
        
        if missing_critical:
            return self.failure_response(query,result, meta={"reason": "missing_critical_fields","fields_missing": missing_critical, "failure_code": sop_id["failure_code"]})
        
        sop_doc = self.collection_sops.get(ids=[sop_id["sop_id"]])
        sop_text = sop_doc["documents"][0]
        prompt = f"""
        YOU MUST FOLLOW THIS SOP STRICTLY:
        {sop_text}

        DATA FOR PRODUCT:
        {product_data}

        USER QUERY: {query}
        
        """
        
        response = ollama.chat(model="mistral:latest", messages=[{"role": "user", "content": prompt}])
        return response["message"]["content"]
    
    def failure_response(self,query,result,meta=None):
        prompt = f"""
        YOU MUST FOLLOW THIS SOP STRICTLY:
        {self.collection_sops.get(ids=["SOP-00"])["documents"][0]}

        USE RESOLVER RESULTS FOR REFUSAL/CLARIFICATION: {result}

        OPTIONAL META DATA (NOT ALWAYS AVAILABLE): {meta}

        USER QUERY: {query}
        
        """
        
        response = ollama.chat(model="mistral:latest", messages=[{"role": "user", "content": prompt}])
        return response["message"]["content"]
    
    def routing(self,query):
        result = self.resolver.resolve(query)

        if result.resolved_product_id is None:
            return self.failure_response(query,result,meta={"reason": "resolver_failed_to_resolve_product"})

        return self.sop_call(query, result)


