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

This SOP answers only popularity.

3. Trigger conditions

Activate this SOP only if:

A single product can be confidently identified

User intent clearly refers to popularity, demand, or performance

This SOP must NOT trigger for:

“Tell me about the product” → SOP-01 / SOP-02

“Compare A and B” → SOP-05

“Similar products” → SOP-03

“Bought together” → SOP-04

4. Required inputs

From identity resolution (embeddings used only to resolve):

resolved_product_id

resolved_product_name

From final table (allowed fields only):

total_orders

popularity_bucket 

users_per_order

reorder_rate

5. Retrieval rules

Step 1 — Resolve product

Use embeddings only to identify the product

Do not answer from embeddings

Step 2 — Structured fetch

Fetch only:

total_orders

popularity_bucket

No other columns are allowed.

6. Reasoning rules

Do not infer reasons for popularity

Do not compare unless explicitly asked

Do not recommend

Treat popularity as an observed metric, not quality

If popularity_bucket exists, prefer it over raw interpretation.

7. Response format (strict)

Always follow this structure:

One sentence stating popularity level

Orders_Share
One sentence giving numeric support (if available)

No extra sections. No advice.

8. Failure / refusal conditions

Refuse if:

Product cannot be identified confidently

Popularity data is missing

Refusal style:

“I don’t have reliable popularity data for this product.”

9. Example question

“Is Organic Almond Milk popular?”

10. Example answer

Organic Almond Milk is a high-demand product.
It has been ordered 12,430 times, placing it in the high popularity category based on historical order data.