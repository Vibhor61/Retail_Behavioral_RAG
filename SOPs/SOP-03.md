SOP-03 — SIMILAR_PRODUCTS
1. Intent it handles

User wants products that are similar in nature or purpose to a given product.

Typical phrases:
"similar products"
"products like this"
"alternatives like this"
"something similar to X"

This SOP answers semantic similarity, not co-purchase behavior.

2. Trigger conditions

Activate this SOP only if:

A single product can be identified confidently

User intent implies similarity, not:

“bought together”

“often purchased with”

“compare A vs B”

“cheaper / better option” (substitution SOP later)

3. Required inputs

From identity resolution:

resolved_product_id

resolved_product_name

From final table:

product_semantic_text (embedded text)

department_name

aisle_name

4. Retrieval rules (this is the heart)
Step 1 — Semantic retrieval (embeddings)

Use product_semantic_text embeddings

Retrieve top N candidates (default N = 5)

Exclude the original product

Embeddings are used only here to measure similarity.

Step 2 — Structured filtering (table constraints)

From the retrieved candidates:

Keep products in the same department

Prefer products in the same aisle

Drop products with missing basic info

This step prevents:

semantically similar but contextually wrong matches
(e.g., almond milk ↔ almond oil)

Step 3 — Final ranking

Rank remaining products by:

embedding similarity score

same aisle > same department > cross-department (if allowed)

5. Reasoning rules

Do not mention popularity unless explicitly asked

Do not say “customers also buy” (that’s SOP-04)

Do not explain similarity using analytics

Explain similarity only using descriptive attributes:

category

usage

material/type

positioning

6. Allowed data fields for explanation

From the table:

product_name

department_name

aisle_name

product_description (or other static attributes)

❌ Not allowed:

total_orders

popularity_bucket

bought_together

7. Response format (strict)

Start with a one-line summary, then list up to 5 products.

For each product:

Product name

One-line explanation of why it’s similar

No scores. No rankings shown.

8. Failure / refusal conditions

Refuse if:

product identity cannot be resolved

no similar products found after filtering

Refusal style:

“I couldn’t find sufficiently similar products for this item in the available data.”

9. Example question

“Show me products similar to Organic Almond Milk.”

10. Example answer

Products similar to Organic Almond Milk include:

Unsweetened Soy Milk — A plant-based milk alternative commonly used as a dairy substitute in beverages and cooking.

Oat Milk Original — A non-dairy milk option with similar usage in cereals and drinks.

Cashew Milk — Another nut-based milk alternative designed for lactose-free diets.

Rice Milk — A plant-derived milk substitute intended for everyday consumption.