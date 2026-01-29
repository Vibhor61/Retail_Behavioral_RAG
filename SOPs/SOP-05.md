SOP-05 — PRODUCT_COMPARISON (A vs B)
1. Intent it handles

User wants to compare two specific products side by side.

Typical phrases:

“compare A and B”

“A vs B”

“difference between A and B”

“which is better” (⚠️ handled carefully)

“how does A differ from B”

This SOP compares facts and observed metrics, not opinions.

2. Trigger conditions

Activate this SOP only if:

Exactly two products are identified confidently

User intent explicitly implies comparison

This SOP must NOT trigger for:

“similar products” → SOP-03

“bought together” → SOP-04

“which should I buy” → recommendation SOP later

If more than two products are mentioned → refuse or ask to narrow (depending on your system choice).

3. Required inputs

From identity resolution (embeddings used only to resolve):

product_id_A

product_id_B

From final table (allowed fields):
Identity & placement

product_name

department_name

aisle_name

Descriptive (if exists)

product_description (only if structured)

Popularity (already defined elsewhere)

popularity_segment

total_orders

Shopping behavior

avg_cart_position

reorder_rate (optional)

Timing (only if aggregated properly)

dominant_day_segment

dominant_hour_segment
hour_segment

Important:
❌ No embeddings used for answering
❌ No bought-together data here

4. Retrieval rules

Step 1 — Resolve both products

Use embeddings to resolve product A and product B independently

If either is ambiguous → refuse

Step 2 — Structured fetch

Fetch allowed fields for both products

Ensure fields are aligned (same metric compared to same metric)

5. Reasoning rules (this matters)

Compare only shared attributes

Do not invent differences

If a metric exists for one product but not the other → say so

Do not declare a “winner” unless the user explicitly asks

If user asks “which is better”:

Reframe as “better in what sense” using available metrics only

No subjective judgement

6. Comparison dimensions (fixed)

Comparisons must follow this order:

Department & aisle

Description / product type

Popularity & demand (if available)

Cart behavior

Ordering patterns (time/day)

Do not add new dimensions dynamically.

7. Response format (strict)

Start with a one-line summary.

Then a side-by-side table-style narrative, section by section.

Example structure:

Products compared: A vs B

Category & placement

A: …

B: …

Description

A: …

B: …

Popularity & demand

A: …

B: …

Shopping behavior

A: …

B: …

Ordering patterns

A: …

B: …

End with a neutral closing sentence.

8. Failure / refusal conditions

Refuse if:

Fewer or more than two products identified

Metrics required for comparison are missing for both

User asks for subjective judgement without measurable basis

Refusal style:

“I can compare factual attributes and observed metrics, but I don’t have enough data to make that comparison here.”

9. Example question

“Compare Organic Almond Milk and Oat Milk Original.”

10. Example answer

Products compared: Organic Almond Milk vs Oat Milk Original

Category & placement

Organic Almond Milk: Dairy Alternatives, Plant-Based Beverages aisle

Oat Milk Original: Dairy Alternatives, Plant-Based Beverages aisle

Description

Organic Almond Milk: Unsweetened almond-based dairy substitute

Oat Milk Original: Oat-derived dairy alternative with a thicker texture

Popularity & demand

Organic Almond Milk: High popularity, 12,430 total orders

Oat Milk Original: Moderate popularity, 9,210 total orders

Shopping behavior

Organic Almond Milk: Avg cart position 4.2

Oat Milk Original: Avg cart position 5.1

Ordering patterns

Organic Almond Milk: Typically ordered later in the day

Oat Milk Original: Ordered evenly across the day

Both products serve similar use cases but differ in demand and cart behavior based on observed transaction data.