SOP-03 — SIMILAR_PRODUCTS
1. Intent it handles

User wants products that are similar in nature or purpose to a given product.

Typical phrases:
"similar products"
"products like this"
"alternatives like this"
"something similar to X"

This SOP answers semantic similarity based on department and aisle proximity, not co-purchase behavior.

2. Trigger conditions

Activate this SOP only if:

Router has selected SOP-03

Resolver has already returned exactly one resolved_product_id

If no similarity is implied this SOP should not be triggered 

Don't trigger when user implies : 
    bought together
    often purchased with
    compare A vs B
    cheaper/better option
    popular/trending


3. Required inputs

From resolver:

resolved_product_id

resolved_product_name


From final table (allowed fields):

product_name

department_name

aisle_name

No other fields are allowed.

4. Retrieval rules (this is the heart)
Step 1 — Fetch resolved product

Retrieve:
  product_name

  department_name

  aisle_name

If any are missing → SOP refusal.

Step 2 — Candidate pool (structured)

Retrieve candidate products:

same department_name (hard constraint)

prefer same aisle_name (soft constraint)

Exclude the original product.

Step 3 — Final selection (deterministic)

Return up to N = 3 using this priority:

same aisle

otherwise same department (only if aisle has < N items)

If you need a tie-breaker within the same aisle/department:

sort by product_name lexicographic (or stable product_id order)

(do not use popularity/order metrics)

5. Reasoning rules

Do not say “customers also buy” (that’s SOP-04)

Do not explain similarity using analytics

Explain similarity only using department and aisle and give answer in probabilistic language not certainty

6. Allowed data fields for explanation

From the table:

product_name

department_name

aisle_name

7. Response format (strict)

Start with a one-line summary. 

Then list up to 3 products.

For each product:

Product name

One-line explanation of why it’s similar

No scores. No rankings shown.

8. Failure / refusal conditions

Fail if:

Refuse only if data is insufficient:

Anchor product missing product_name, department_name, or aisle_name

Candidate pool empty after applying constraints

Return:
{
  "status": "fail",
  "failure_type": "NO_VALID_SIMILAR_PRODUCTS",
  "reason": "insufficient_category_data_or_empty_candidate_pool",
  "missing_fields": <department_name|aisle_name>
}

9. Example question

“Show me products similar to Organic Almond Milk.”

10. Example answer

# No more product description available 
Products similar to Organic Almond Milk include:

Unsweetened Soy Milk — Another “milk” alternative listed in the same Plant-Based Beverages aisle.

Oat Milk Original — A “milk” product in the same aisle and department category.

Cashew Milk — Another nut-based “milk” item from the same aisle category.