SOP-02: Product Detailed Profile
1. SOP Number & Name

SOP-02 — PRODUCT_DETAILED_PROFILE

2. Intent it handles

User wants more details about a specific product after identification.

Typical phrases:

“more details”

“tell me everything”

“full details”

“describe it properly”

“give complete info”

This goes beyond identification but is not for analytic or recommendation

3. Trigger conditions

Trigger only if:

Router has selected SOP-02
Resolver has already returned exactly one resolved_product_id

User explicitly requests more detail (“more details”, “full profile”, “everything”)

This SOP must NOT trigger if the user asks specifically for:

"basic info" -> SOP Basic Info

“bought together” → SOP bought-together

“similar products” → SOP similar

“compare A vs B” → SOP comparison

“trend/when/behavior” → SOP shopping behavior or SOP product popularity


4. Required inputs

From resolver (assumed valid — not rechecked here):

resolved_product_id


From final table (allowed fields for this SOP):

Identity:(Mandatory)
    product_name
    department_name
    aisle_name

Popularity & volume:
    total_orders
    popularity_segment
    popularity_rank

Repeat behavior:
    reorder_rate
    repeat_user_count
    orders_per_users

Temporal behavior:
    dominant_day
    dominant_hour

Evidence:
    early_week_percent, mid_week_percent, weekend_percent
    morning_percent, afternoon_percent, evening_percent, night_percent

Cart behavior
    avg_cart_position
    cart_position_segment

Co-purchase:
    bought_together_names
    counts_of_bought_together (top-k default = 3)

No other fields are allowed.


5. Retrieval rules

Step 1 — Resolve product
Use resolved_product_id to query the final table

Step 2 — Fetch product profile

Fetch only allowed fields

If non-core fields are missing/null → omit their sections

Do not infer or fabricate missing values

6. Reasoning rules

Do not invent details not present in table

If a metric is missing/null, say “not available” or omit section

Keep analytics as observations, not claims of causality


7. Response format (strict)

Always output in these sections in this order:

Product
    Name
    Department
    Aisle

Popularity and Volume:
    total_orders
    popularity_segment
    popularity_rank

Shopping behavior:
    reorder_rate
    repeat_user_count
    orders_per_users

Temporal behavior:
    dominant_day with count
    dominant_hour with count 

Cart behavior
    avg_cart_position
    cart_position_segment

Co-purchase:
    bought_together_names with counts_of_bought_together (top-k default = 3)
    
No extra sections

8. Failure / refusal conditions

Refuse if:

product_name

department_name

aisle_name

Return 
Refusal style:
{
  "status": "fail",
  "failure_type": "INSUFFICIENT_PRODUCT_PROFILE",
  "reason": "missing_core_identity_fields",
  "missing_fields": ["product_name", "department_name", "aisle_name"],
}

9. Example question

“Tell me more details about Organic Almond Milk. Everything you have.”

10. Example answer (template)

Product
Name: Organic Almond Milk
Department: Dairy Alternatives
Aisle: Plant-Based Beverages

Popularity and Volume:
Total orders: 12,430
Popularity segment: High
Popularity rank: 118

Shopping behavior:
Reorder rate: 61%
Repeat user count: 4,982
Orders per user: 2.49

Temporal behavior:
Dominant day: Weekend (8,950 orders)
Dominant hour: Evening (5,972 orders)

Cart behavior:
Average cart position: 4.2
Cart position segment: Early

Co-purchase:
Bananas (3,214), Oats (2,887), Peanut Butter (2,103)
