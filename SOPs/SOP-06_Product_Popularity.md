SOP-06 — PRODUCT_POPULARITY
1. SOP Number & Name

SOP-06 — PRODUCT_POPULARITY

2. Intent it handles

User is explicitly asking about popularity / demand of a product.

Typical user phrases:

“Is this product popular?”

“How well does this product sell?”

“Is this a high-demand product?”

“What is the popularity of this product?”

This SOP answers only popularity , no recommendation.

3. Trigger conditions

Activate this SOP only if:

Router has selected SOP-06

Resolver has already returned exactly one resolved_product_id

User intent clearly refers to popularity, demand, or performance

This SOP must NOT trigger for:

product description → SOP-01 / SOP-02

comparison → SOP-05

similar products → SOP-03

bought together → SOP-04

4. Required inputs

From resolver (assumed valid):

resolved_product_id



From final table (allowed fields only):

total_orders

popularity_segment

popularity_rank

reorder_rate 

No other fields are allowed.

5. Retrieval rules

Step 1 — Resolve product

Use resolved_product_id

Step 2 — Structured fetch

Fetch only:

total_orders

popularity_segment

popularity_rank

reorder_rate

6. Reasoning rules

Do not infer reasons for popularity

Do not compare unless explicitly asked

Do not recommend

Use popularity_rank and popularity_segment as primary signal use total_orders and reorder_rate as numeric support

7. Response format (strict)

Always follow this structure:

Sentence 1:
State popularity level using popularity_segment and popularity_rank 

Sentence 2:
Provide numeric support using total_orders and reorder_rate.

No extra sections. No advice.

8. Failure / refusal conditions

Refuse if:

total_orders missing or null

popularity_segment missing or null

Return:

{
  "status": "fail",
  "failure_type": "NO_POPULARITY_DATA",
  "reason": "missing_popularity_fields",
}

No user-facing refusal text here.

9. Example question

“Is Organic Almond Milk popular?”

10. Example answer

Organic Almond Milk is a high-popularity product and ranks 118th overall in demand.
It has 12,430 total orders with a 61% reorder rate, based on historical transaction data.