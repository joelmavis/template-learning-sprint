# L01 · Rows, columns, and data types

- Status: completed

## Learning objectives

- State the grain of a table.
- Classify numeric, date, categorical, and Boolean fields.

## Learning content

A reliable analysis begins by saying what one row represents. In the bundled order table, one row is intended to represent one order. `units` and `unit_price` are numeric; `date` is temporal; `channel` and `region` are categorical; `returned` is Boolean-like. `order_id` is an identifier even though it contains letters and digits.

## Practice

State the intended grain and classify `order_id`, `date`, `units`, and `channel`.

## Learner submission

One row is one order. order_id is text, date is a date, units is numeric, and channel is a category.

## Feedback

The classifications are correct. Calling `order_id` merely text misses its role: it is an identifier and should be checked for uniqueness at this grain.

## Adaptation

Add uniqueness checking to the cleaning lesson.
