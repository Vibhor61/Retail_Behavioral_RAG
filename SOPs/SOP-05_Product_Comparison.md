SOP-05 — PRODUCT_COMPARISON (A vs B)
1. Intent it handles

User wants to compare two specific products side by side.

Typical phrases:

“compare A and B”

“A vs B”

“difference between A and B”

“which is better (handled using available metrics only) "

“how does A differ from B”

This SOP compares facts and observed metrics, not opinions.

2. Trigger conditions

Router has selected SOP-05

Resolver has already returned exactly two resolved product IDs

User intent explicitly implies comparison

This SOP must NOT trigger for:
    bought together
    which should I buy
    similar product
    often purchased with
    information about product
    popular / trending

3. Required inputs

From resolver (assumed valid):
    resolved_product_id_A
    resolved_product_id_B

From final table (allowed for each product):

Identity(mandatory):
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

Cart behavior:
    avg_cart_position
    cart_position_segment

Not allowed in this SOP:
    bought_together_names
    counts_of_bought_together

No other fields are allowed.

4. Retrieval rules

Step 1 — Resolve both products

Use resolved_product_id_A and resolved_product_id_B to fetch allowed fields

Step 2 — Structured fetch

Fetch the allowed fields above for both products from the final table.

Ensure fields are aligned (same metric compared to same metric)

If a field is missing for one product, mark it as “not available” for that product only.

Do not infer or backfill missing values

5. Reasoning rules 

Compare only the predefined attributes in this SOP; if a value is missing for one product, mark it as "not available"

Do not invent differences or explanations 

If user asks "which is better": 
    If the user asks “which is better” without naming a metric, do not declare a winner

    If a metric is named, winner may be stated only for that metric

6. Comparison dimensions (fixed)

Always compare in this order:

Category and placement

department_name, aisle_name

Popularity and volume

total_orders, popularity_segment, popularity_rank

Repeat behavior

reorder_rate, repeat_user_count, orders_per_users

Cart behavior

avg_cart_position, cart_position_segment

Temporal behavior

dominant_day, dominant_hour

Temporal evidence shares

early/mid/weekend

morning/afternoon/evening/night

No new dimensions may be added dynamically.


7. Response format (strict)

Start with a one-line summary.

Then present section-by-section comparison in the fixed order:

Products compared: Product A vs Product B

Category and placement
A: department_name, aisle_name
B: department_name, aisle_name

Popularity and volume
A: total_orders; popularity_segment; popularity_rank
B: total_orders; popularity_segment; popularity_rank

Repeat behavior
A: reorder_rate; repeat_user_count; orders_per_users
B: reorder_rate; repeat_user_count; orders_per_users

Cart behavior
A: avg_cart_position; cart_position_segment
B: avg_cart_position; cart_position_segment

Temporal behavior
A: dominant_day; dominant_hour
B: dominant_day; dominant_hour

Temporal evidence shares
A: early/mid/weekend; morning/afternoon/evening/night
B: early/mid/weekend; morning/afternoon/evening/night

Closing sentence (fixed):

This comparison is based on observed aggregate transaction metrics and placement metadata.

8. Failure / refusal conditions

Refuse if:

Fewer or more than two products provided to this SOP

Missing core identity fields (product_name, department_name, aisle_name) for either product

Both products lack all comparable metrics beyond identity

Return:
{
  "status": "fail",
  "failure_type": "COMPARISON_NOT_POSSIBLE",
  "reason": "invalid_input_count_or_insufficient_shared_metrics"
}


9. Example question

“Compare Organic Almond Milk and Oat Milk Original.”

10. Example answer

Products compared: Organic Almond Milk vs Oat Milk Original

Category and placement
Organic Almond Milk: Dairy Alternatives, Plant-Based Beverages
Oat Milk Original: Dairy Alternatives, Plant-Based Beverages

Popularity and volume
Organic Almond Milk: Total orders 12,430; Popularity segment High; Popularity rank 118
Oat Milk Original: Total orders 9,210; Popularity segment Medium; Popularity rank 204

Repeat behavior
Organic Almond Milk: Reorder rate 61%; Repeat user count 4,982; Orders per user 2.49
Oat Milk Original: Reorder rate 54%; Repeat user count 3,910; Orders per user 2.12

Cart behavior
Organic Almond Milk: Avg cart position 4.2; Cart position segment Early
Oat Milk Original: Avg cart position 5.1; Cart position segment Mid

Temporal behavior
Organic Almond Milk: Dominant day Weekend; Dominant hour Evening
Oat Milk Original: Dominant day Mid-week; Dominant hour Afternoon

Temporal evidence shares
Organic Almond Milk: Early-week 22%, Mid-week 35%, Weekend 43%; Morning 18%, Afternoon 24%, Evening 41%, Night 17%
Oat Milk Original: Early-week 26%, Mid-week 41%, Weekend 33%; Morning 21%, Afternoon 30%, Evening 34%, Night 15%

This comparison is based on observed aggregate transaction metrics and placement metadata.
