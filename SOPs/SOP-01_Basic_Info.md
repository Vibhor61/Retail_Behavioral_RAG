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

User intent is descriptive

Exactly one product can be identified

No keywords related to:

popularity

comparison

recommendation

trends

performance

This SOP has lowest analytical scope and highest priority for basic product queries.

No other SOP's should be activated 

4. Required inputs

From semantic resolution (embeddings):

resolved_product_id

resolved_product_name

From structured table:

product_name

department_id

department_name

aisle_id

aisle_name

No other fields are allowed.

5. Retrieval rules

Step 1 — Product resolution

Use embeddings only to resolve the product identity.

Do not answer from embeddings.

Step 2 — Structured fetch

Fetch only the following columns from the final table:

product_name

department_name

aisle_name


6. Reasoning rules

Do not infer use cases

Do not summarize beyond naming

Do not add marketing language

This SOP is pure identification.


7. Response format

Always exactly this structure:

Product name (bold)

One sentence stating department and aisle

No bullet points. No extra context.


8. Failure / refusal conditions

Refuse if:

Product cannot be resolved confidently

Multiple products match equally

Department or aisle data is missing

Refusal style:

“I can’t reliably identify this product with the available information.


9. Example question

“Tell me about Organic Almond Milk”

10. Example answer

Organic Almond Milk belongs to the Dairy Alternatives department and is placed in the Plant-Based Beverages aisle.