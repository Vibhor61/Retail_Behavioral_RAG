import pandas as pd
import numpy as np
from collections import defaultdict

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

def days(x):
    if x in [0, 1, 2]:
        return "Early week"
    elif x in [3, 4]:
        return "Mid week"
    else:  # 5,6
        return "Weekend"


def hours(x):
    if x <= 6:
        return "morning"
    elif x <= 12:
        return "afternoon"
    elif x <= 18:
        return "evening"
    else:
        return "night"


if __name__ == "__main__":
    
    aisles = pd.read_csv("Data\aisles.csv")
    departments = pd.read_csv("Data\departments.csv")
    products_prior = pd.read_csv("Data\order_products__prior.csv")
    products_train = pd.read_csv("Data\order_products__train.csv")
    orders = pd.read_csv("Data\orders.csv")
    products = pd.read_csv("Data\products.csv")

    
    products_enriched = products.merge(aisles, on='aisle_id', how='left').merge(departments, on='department_id', how='left')

    #product_id	product_name	aisle_id	department_id	aisle	department

    orders["day_wise_segment"] = orders["order_dow"].apply(days)
    orders["hour_wise_segment"] = orders["order_hour_of_day"].apply(hours)
    order_products = pd.concat([products_prior, products_train], axis=0, ignore_index=True)
    order_products = order_products.merge(orders, on='order_id', how='left')

    #order_id  product_id  add_to_cart_order  reordered day_wise_segment hour_wise_segment

    orders_products_list = order_products.groupby('order_id')['product_id'].apply(list)
    bought_together = defaultdict(lambda: defaultdict(int))
    for products_in_order in orders_products_list:
        for i, p1 in enumerate(products_in_order):
            for j, p2 in enumerate(products_in_order):
                if p1 != p2:
                    bought_together[p1][p2] += 1

    top_co_purchased = {product: [p for p, _ in sorted(co_dict.items(), key=lambda x: x[1], reverse=True)[:3]]
                        for product, co_dict in bought_together.items()}
    products_enriched['bought_together'] = products_enriched['product_id'].map(top_co_purchased)
    
    id_to_name = dict(zip(products_enriched['product_id'], products_enriched['product_name']))
    products_enriched['bought_together_names'] = products_enriched['bought_together'].apply(lambda x: ids_to_names(x, id_to_name))

    #product_id	product_name	aisle_id	department_id	aisle	department order_id  product_id  add_to_cart_order  reordered bought_together bought_together_names
    products_enriched = (
        products_enriched
        .merge(
            order_products.groupby('product_id')['add_to_cart_order']
            .mean()
            .reset_index(name='avg_cart_position'), 
            on='product_id', 
            how='left'
            )
        .merge(
            order_products.groupby('product_id')
            .size()
            .reset_index(name='total_orders'),
            on='product_id', 
            how='left'
            )
        .merge(
            order_products.groupby('product_id')['user_id']
            .nunique()
            .reset_index(name='unique_users'),
            on='product_id',
            how='left'
            )
        .merge(
            order_products.groupby('product_id')['reordered']
            .mean()
            .reset_index(name='reorder_rate'),
            on='product_id',
            how='left'
            )
    )

    # product_id	product_name	aisle_id	department_id	aisle	department order_id  \
    # product_id  add_to_cart_order  reordered bought_together bought_together_names \
    # avg_cart_position 'total_orders unique_users reorder_rate log_total_orders popularity_segment cart_position_segment \
    # day_wise_segment hour_wise_segment reorder_rate



    products_enriched["log_total_orders"] = np.log1p(products_enriched["total_orders"])
    p25_orders = products_enriched["log_total_orders"].quantile(0.25)
    p75_orders = products_enriched["log_total_orders"].quantile(0.75)
    products_enriched["popularity_segment"] = products_enriched["log_total_orders"].apply(lambda x: popularity_bucket(x, p25_orders, p75_orders))


    p25_cart = products_enriched["avg_cart_position"].quantile(0.25)
    p75_cart = products_enriched["avg_cart_position"].quantile(0.75)
    products_enriched["cart_position_segment"] = products_enriched["avg_cart_position"].apply(lambda x: cart_position_bucket(x, p25_cart, p75_cart))

    