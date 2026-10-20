# L04 · Filtering and grouped summaries

- Status: completed

## Learning objectives

- Filter rows, group by a dimension, and calculate gross revenue.

## Learning content

Apply cleaning rules first, then calculate row revenue as `units × unit_price`. After removing the duplicated O106, gross revenue is: web 50 + 45 + 60 = 155; store 40 + 200 + 48 = 288; partner 50. Grouped totals answer a different question from average unit price.

## Practice

Calculate gross revenue by channel after applying the L03 rules.

## Learner submission

Web = 215, store = 288, partner = 50. Store is highest.

## Feedback

Store and partner are correct. Web double-counted O106; after deduplication it is 155. The conclusion remains store, but the error matters because it changes the margin.

## Adaptation

Keep duplicate handling visible in every summary.
