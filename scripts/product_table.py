import pandas as pd
import numpy as np
from collections import defaultdict
from pathlib import Path
import re

def ids_to_names(id_list, id_to_name):
    if id_list is None:
        return []
    return [id_to_name[i] for i in id_list]

def popularity_bucket(orders, p25, p75):
    if orders <= p25:
        return "low"
    elif orders >= p75:
        return "high"
    return "moderate"

def cart_position_bucket(pos, p25, p75):
    if pos <= p25:
        return "early"
    elif pos >= p75:
        return "late"
    return "mid"

def day_by_segment(x):
    if x in [1, 2]:
        return "Early week"
    elif x in [3, 4, 5]:
        return "Mid week"
    else:  # 6,0
        return "Weekend"


def hour_by_segment(x):
    if x <= 6:
        return "morning"
    elif x>6 and x<= 12:
        return "afternoon"
    elif x>12 and x<= 18:
        return "evening"
    else:
        return "night"


def normalize(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"[\s\-_]+", " ", s)
    s = re.sub(r"[^\w\s]", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

if __name__ == "__main__":
    #Loading CSV's
    BASE_DIR = Path(__file__).resolve().parent.parent
    DATA_DIR = BASE_DIR / "Data"
    aisles = pd.read_csv(DATA_DIR / "aisles.csv")
    departments = pd.read_csv(DATA_DIR / "departments.csv")
    products_prior = pd.read_csv(DATA_DIR / "order_products__prior.csv")
    products_train = pd.read_csv(DATA_DIR / "order_products__train.csv")
    orders = pd.read_csv(DATA_DIR / "orders.csv")
    products = pd.read_csv(DATA_DIR / "products.csv")



    # Merging aisles and departmnet table with products table
    products_enriched = (
        products
        .merge(aisles, on='aisle_id', how='left')
        .merge(departments, on='department_id', how='left')
    )

    # Concatenating all orders 
    order_products = pd.concat([products_prior, products_train], axis=0, ignore_index=True)
    order_products = order_products.merge(orders, on='order_id', how='left')

    #Popularity Features
    product_features = order_products.groupby('product_id').agg(
        total_orders=('order_id', 'count'),
        unique_users=('user_id', 'nunique'),
        reorder_rate=('reordered', 'mean'),
        avg_cart_position=('add_to_cart_order', 'mean')
    ).reset_index()
  
    products_enriched = products_enriched.merge(product_features , on='product_id', how='left')

    temp_op = order_products[["product_id","order_hour_of_day","order_dow"]].copy()
    temp_op["hour_segment"] = temp_op["order_hour_of_day"].apply(hour_by_segment)
    temp_op["day_segment"] = temp_op["order_dow"].apply(day_by_segment)

    hour_count = (
        temp_op.groupby(["product_id","hour_segment"])
        .size()
        .unstack(fill_value=0)
        .rename(columns={"morning":"morning_count","afternoon":"afternoon_count","evening":"evening_count","night":"night_count"})
        .reset_index()   
    )
    day_count = (
        temp_op.groupby(["product_id","day_segment"])
        .size()
        .unstack(fill_value=0)
        .rename(columns={"Early week":"early_week_count","Mid week":"mid_week_count","Weekend":"weekend_count"})
        .reset_index()
    )

    
    products_enriched = products_enriched.merge(hour_count ,on="product_id", how="left")
    products_enriched = products_enriched.merge(day_count, on='product_id', how='left')
    
    products_enriched["total_orders"] = products_enriched["total_orders"].fillna(0)
    products_enriched["unique_users"] = products_enriched["unique_users"].fillna(0)
    products_enriched["reorder_rate"] = products_enriched["reorder_rate"].fillna(0.0)
    products_enriched["avg_cart_position"] = products_enriched["avg_cart_position"].fillna(0.0)

    products_enriched["log_total_orders"] = np.log1p(products_enriched["total_orders"])
    p25_orders = products_enriched["log_total_orders"].quantile(0.25)
    p75_orders = products_enriched["log_total_orders"].quantile(0.75)

    products_enriched["popularity_segment"] = products_enriched["log_total_orders"].apply(
        lambda x: popularity_bucket(x, p25_orders, p75_orders)
    )
    

    products_enriched["popularity_rank"] = products_enriched["total_orders"].rank(method="dense", ascending=False).astype(int)
    
    #Bought Together 
    orders_products_list = order_products.groupby('order_id')['product_id'].apply(list)
    
    bought_together = defaultdict(lambda: defaultdict(int))
    for products_in_order in orders_products_list:
        for i, p1 in enumerate(products_in_order):
            for j, p2 in enumerate(products_in_order):
                if p1 != p2:
                    bought_together[p1][p2] += 1

    top_co_purchased = {
        product: [co_product for co_product, count in sorted(co_dict.items(), key=lambda x: x[1], reverse=True)[:3]]
        for product, co_dict in bought_together.items()
    }
    
    top_co_purchased_count = {
        product: [count for co_product, count in sorted(co_dict.items(), key=lambda x: x[1], reverse=True)[:3]]
        for product, co_dict in bought_together.items()
    }
    
    products_enriched['bought_together'] = products_enriched['product_id'].map(top_co_purchased)
    products_enriched['counts_of_bought_together'] = products_enriched['product_id'].map(top_co_purchased_count)
    
    id_to_name = dict(zip(products_enriched['product_id'], products_enriched['product_name']))
    products_enriched['bought_together_names'] = products_enriched['bought_together'].apply(
        lambda x: ids_to_names(x, id_to_name)
    )
    #products_enriched.drop(columns=['bought_together'])

    #Repeating User / Orders-per-User
    products_enriched["repeat_user_count"] = (products_enriched["total_orders"] - products_enriched["unique_users"]).clip(lower=0)
    den_users = products_enriched["unique_users"].replace(0, np.nan)
    products_enriched["orders_per_users"] = (products_enriched["total_orders"] / den_users).fillna(0)

    #Cart Position Segment
    p25_cart = products_enriched["avg_cart_position"].quantile(0.25)
    p75_cart = products_enriched["avg_cart_position"].quantile(0.75)
    products_enriched["cart_position_segment"] = products_enriched["avg_cart_position"].apply(
        lambda x: cart_position_bucket(x, p25_cart, p75_cart)
    )

    for col in ["early_week_count","mid_week_count","weekend_count","morning_count","afternoon_count","evening_count","night_count"]:
        if col not in products_enriched.columns:
            products_enriched[col] = 0
        products_enriched[col] = pd.to_numeric(products_enriched[col], errors="coerce").fillna(0).astype(int)
            
    #Day Segment and percentage
    denom = products_enriched["total_orders"].replace(0,np.nan)
    products_enriched["early_week_percent"] = (products_enriched["early_week_count"]/denom).fillna(0.0)
    products_enriched["mid_week_percent"] = (products_enriched["mid_week_count"]/denom).fillna(0.0)
    products_enriched["weekend_percent"] =( products_enriched["weekend_count"]/denom).fillna(0.0)
    
    products_enriched["dominant_day"] = products_enriched[["early_week_percent","mid_week_percent","weekend_percent"]].idxmax(axis=1)
    products_enriched["dominant_day"] = products_enriched["dominant_day"].str.replace('_percent','')
    
    #Hour Segment and percentage
    products_enriched["morning_percent"] = (products_enriched["morning_count"]/denom).fillna(0.0)
    products_enriched["afternoon_percent"] = (products_enriched["afternoon_count"]/denom).fillna(0.0)
    products_enriched["evening_percent"] = (products_enriched["evening_count"]/denom).fillna(0.0)
    products_enriched["night_percent"] = (products_enriched["night_count"]/denom).fillna(0.0)

    products_enriched["dominant_hour"] = products_enriched[["morning_percent","afternoon_percent","evening_percent","night_percent"]].idxmax(axis=1)
    products_enriched["dominant_hour"] = products_enriched["dominant_hour"].str.replace('_percent','')

    products_enriched["norm_name"] = products_enriched["product_name"].map(normalize)

    products_enriched.drop(
    columns=[
        "aisle_id",
        "department_id",
        "order_id",
        "user_id",
        "add_to_cart_order",
        "reordered",
        "order_dow",
        "order_hour_of_day",
        "day_segment",
        "hour_segment",
        "log_total_orders",
        "bought_together"
    ],
    inplace=True,
    errors="ignore"
    )

    
    products_enriched["Embeddings card"] =  (
        "Product : "+ products_enriched["product_name"]  +
        "\nAisle : " + products_enriched["aisle"] +
        "\nDepartment : " + products_enriched["department"] 
    )

    output_path = Path("Data") / "Final_Table.parquet"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    products_enriched.to_parquet(output_path, index=False)
