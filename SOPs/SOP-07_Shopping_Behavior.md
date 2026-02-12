SOP-07: Product Shopping Behavior
1. SOP Number & Name

SOP-07 — PRODUCT_SHOPPING_BEHAVIOR

2. Intent it handles

User asks the behavior pattern of how a product is shopped

Typical phrases:

"how much product is bought"

"how many people reorder product X"

"frequency of product bought"


3. Trigger conditions

Trigger only if:

Router has selected SOP-07

Resolver has already returned exactly one resolved_product_id

User intent explicitly asks about shopping frequency, repeat behavior, or buyer patterns

Must NOT trigger for:

basic info → SOP-01

detailed profile → SOP-02

popularity / demand → SOP-06

bought together → SOP-04

similar products → SOP-03

comparison → SOP-05


4. Required inputs

From resolver (assumed valid):

resolved_product_id

From final table (allowed fields only):

Identity (mandatory):

product_name

department_name

aisle_name

Shopping behavior metrics:

total_orders

popularity_bucket

unique_users

reorder_rate

orders_per_users

avg_cart_position

cart_position_segment

No other fields are allowed.


5. Retrieval rules

Step 1 — Resolve product

Use resolved_product_id

Step 2 — Structured fetch

Fetch only the allowed fields listed above

If any metric is missing, mark it as "Not Available" (do not hallucinate)

6. Reasoning rules

Do not invent details not present in table

If a metric is missing/null, say “not available” or omit section

Do not recommend or compare

Treat all metrics as observed aggregates


7. Response format (strict)

Always output in the following order:

Product:

Name

Department

Aisle

Shopping behavior:

Total orders

Popularity bucket

Unique users

Reorder rate

Orders per user

Average cart position

Cart position segment

No extra sections. No advice.

8. Failure / refusal conditions

Fail if :

Missing any identity fields

All shopping behavior metrics are missing or null

Return:

{
  "status": "fail",
  "failure_type": "NO_SHOPPING_BEHAVIOR_DATA",
  "reason": "missing_identity_or_behavior_metrics",
}


No user-facing refusal text here.

9. Example question

"How do people usually buy Organic Almond Milk?”

10. Example answer (template)

Product
Name: Organic Almond Milk
Department: Dairy Alternatives
Aisle: Plant-Based Beverages

Shopping behavior
Total orders: 12,430
Popularity bucket: High
Unique users: 6,120
Reorder rate: 61%
Orders per user: 2.49
Average cart position: 4.2
Cart position segment: Early
