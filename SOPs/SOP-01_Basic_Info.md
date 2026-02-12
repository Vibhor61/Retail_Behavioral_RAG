1. SOP Number & Name

SOP-01 — PRODUCT_BASIC_INFO

2. Intent it handles

User is asking about a product, nothing analytical, nothing comparative.

This SOP answers:

"Product X"
"What is this product?"
"About product X”
“Which department / aisle is this product in?


3. Trigger conditions

Activate only if:

Router has selected SOP-01
Resolver returned exactly one product (resolved_product_id present; not ambiguous/no_match)
User intent is descriptive

No keywords related to:
popularity
comparison
recommendation
trends
performance
behavior

This SOP has lowest analytical scope and highest priority for basic product queries.

If any analytical intent SOP-01 must not be activated


4. Required inputs

From product resolution layer (lexical/fuzzy or embeddings):
resolved_product_id is not null
resolved_product_name is not null
resolver failure_reason is null

From structured table:
product_name
department_name
aisle_name

No other output fields are allowed.

5. Retrieval rules

Use resolved_product_id to fetch only:
product_name
department_name
aisle_name

Use resolved_product_name from resolver as the display name; do not re-resolve product name.


6. Reasoning rules

Do not infer use cases

Do not summarize beyond naming

Do not add marketing language

This SOP is pure identification.


7. Response format

Always exactly this structure:

Line 1 : Product name (bold)

Line 2: This belongs to the {department_name} department and is placed in the {aisle_name} aisle.

No summarization beyond identification fields


8. Failure / refusal conditions

Refuse if:

Department or aisle data is missing

Return 

{
  "status": "fail",
  "failure_type": "MISSING_DATA",
  "reason": "required_fields_are_missing",
  "missing_fields": "<product_name|department_name|aisle_name>"
}
(Include only the fields actually missing)

9. Example question

“Tell me about Organic Almond Milk”

10. Example answer

Organic Almond Milk
It belongs to the Dairy Alternatives department and is placed in the Plant-Based Beverages aisle.