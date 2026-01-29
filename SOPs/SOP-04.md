SOP-04 — FREQUENTLY_BOUGHT_TOGETHER
1. Intent it handles

User wants to know which products are commonly purchased together with a given product.

Typical phrases:

“frequently bought together”

“often bought with”

“customers also buy”

“paired with”

“usually purchased along with”

This SOP handles behavioral association, not similarity.

2. Trigger conditions

Activate this SOP only if:

A single product is confidently identified

User intent clearly implies co-purchase behavior

This SOP must NOT trigger for:

“similar products” → SOP-03

“alternatives” → substitution SOP later

“compare products” → comparison SOP

“popular products” → popularity SOP

3. Required inputs

From identity resolution:

resolved_product_id

resolved_product_name

From final table:

bought_together_ids

bought_together_names

co_occurrence_strength (if you have it)

Embeddings are not used in this SOP after product resolution.

4. Retrieval rules

Step 1 — Resolve product

Use embeddings only to identify the product

No answering from embeddings

Step 2 — Structured retrieval

Fetch from the final table:

bought_together_names (top_k, default = 5)

co_occurrence_strength (if available)

No semantic search.
No similarity scoring.

5. Reasoning rules

Do not infer “why” beyond simple context

Do not claim similarity

Do not recommend substitutes

If confidence is weak, say so explicitly

Language must reflect observed behavior, not intent or causality.

6. Allowed data fields for explanation

From the table only:

product_name

bought_together_names

co_occurrence_strength (optional)

❌ Not allowed:

embeddings

popularity_bucket

total_orders

descriptive similarity

7. Response format (strict)

Start with a one-line summary.

Then list up to 5 products, ordered by co-occurrence strength.

For each item:

Product name

Short neutral explanation (e.g. “commonly purchased in the same order”)

If strength exists:

mention it as high / medium / low

8. Failure / refusal conditions

Refuse if:

product cannot be identified confidently

no co-purchase data exists for the product

Refusal style:

“I don’t have reliable co-purchase data for this product.”

9. Example question

“What is frequently bought together with Organic Almond Milk?”

10. Example answer

Customers who purchase Organic Almond Milk often buy the following items in the same order:

Bananas — frequently purchased together in grocery baskets (high association)

Oats — commonly paired for breakfast-related purchases (medium association)

Peanut Butter — often included in similar orders (medium association)

Whole Grain Bread — occasionally bought together (low association)

These associations are based on historical transaction co-occurrence, not product similarity.