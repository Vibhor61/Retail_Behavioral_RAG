SOP-02: Product Shopping Behavior
1. SOP Number & Name

SOP-02 — PRODUCT_SHOPPING_BEHAVIOR

2. Intent it handles

User asks the behavior pattern of how a product is shopped

Typical phrases:

"how much product is bought"

"popularity of product"

"how many people reorder product X"

"frequency of product bought"


3. Trigger conditions

Trigger only if:

A product is already identified confidently OR can be identified confidently from the request

User explicitly asks how th product is shopped

This SOP must NOT trigger if the user asks specifically for:

"basic info" -> SOP Basic Info

“bought together” → SOP bought-together

“similar products” → SOP similar

“compare A vs B” → SOP comparison

“trend / peak time” → SOP timing/trend SOP



4. Required inputs

From identity resolution (embeddings used only to resolve):

resolved_product_id

From final table (allowed fields for this SOP):

Identity & placement

product_id

product_name

department_name

aisle_name

total_orders

popularity_bucket

cart_position_segmnet

reorder_rate

unique_users

orders_per_users


5. Retrieval rules

Step 1 — Resolve product

embeddings: resolve product_id (no answering from embeddings)

Step 2 — Fetch product profile

query final table for the allowed fields above

if some fields are missing, skip those sections (don’t hallucinate)

6. Reasoning rules

Do not invent details not present in table

If a metric is missing/null, say “not available” or omit section

Keep analytics as observations, not claims of causality

If bought_together exists, present it as “often purchased with”

7. Response format (strict)

Always output in these sections in this order:

Product

Name, Department, Aisle

Description

Only if product_description exists

Shopping behavior

total_orders

popularity_bucket

avg_cart_position (interpret as early/mid/late only if you’ve defined buckets elsewhere; otherwise show the number plainly)

When it’s typically ordered

avg_order_hour

avg_order_day

Often purchased with

top 5 bought_together_names (if present)

No extra sections. No recommendations.

8. Failure / refusal conditions

Refuse if:

product cannot be resolved confidently

table lacks even basic fields (name/department/aisle)

Refusal style:

“I can’t reliably define shopping behavior related to this product.”

9. Example question

"Tell me about how many people buy Organic Almond Milk"

10. Example answer (template)

Product: Organic Almond Milk
Department: Dairy Alternatives
Aisle: Plant-Based Beverages

Description: Unsweetened almond-based milk intended as a dairy substitute.

Shopping behavior:
Total orders: 12,430
Popularity: High
Avg cart position: 4.2
