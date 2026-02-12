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

Router has selected SOP-04

Resolver has already returned exactly one resolved_product_id

User intent clearly implies co-purchase behavior

Don't trigger when user implies : 
    similar product
    often purchased with
    compare A vs B
    information about product
    popular / trending


3. Required inputs

From resolver :

resolved_product_id


From final table:

bought_together_names
    
counts_of_bought_together (top-k default = 3)

No other fields are allowed.


4. Retrieval rules

Step 1 — Resolve product

Use resolved_product_id to fetch product_name

Step 2 — Structured retrieval

Fetch from final table:

bought_together_names

counts_of_bought_together

No semantic search.
No similarity logic.

5. Reasoning rules

Do not explain why items are purchased together

Do not claim similarity

Do not recommend substitutes

Language must reflect observed co-occurrence only

Strength may be described relatively (higher / lower) using counts


6. Allowed data fields for explanation

From the table only:

product_name

bought_together_names

counts_of_bought_together


7. Response format (strict)

Start with a one-line summary of resolved_product

Then use bought_together_names ordered by counts_of_bought_together 

For each item:

Product name

Short neutral explanation (e.g. “commonly purchased in the same order”) with counts 

Allowed verb variants (choose one per item, based only on relative rank):

“commonly purchased together”

“frequently included in the same order”

“often bought alongside”


8. Failure / refusal conditions

Refuse if :

bought_together_names is null or empty

counts_of_bought_together missing, empty, or length-mismatched

Return :

{
  "status": "fail",
  "failure_type": "NO_COPURCHASE_DATA",
  "reason": "bought_together_fields_missing_or_empty"
}

9. Example question

“What is frequently bought together with Organic Almond Milk?”

10. Example answer

Customers who purchase Organic Almond Milk often buy the following items in the same order:

Bananas — commonly purchased together (3,214 co-occurring orders)

Oats — frequently included in the same order (2,887 co-occurring orders)

Peanut Butter — often bought alongside (2,103 co-occurring orders)

These associations reflect historical transaction co-occurrence, not product similar