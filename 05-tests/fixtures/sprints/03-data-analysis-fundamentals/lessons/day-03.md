# L03 · Missing values and duplicates

- Status: completed

## Learning objectives

- Identify missing and duplicate records.
- Choose a documented handling rule.

## Learning content

Cleaning is a decision, not automatic deletion. The table contains a missing `region` for O105 and a duplicated O106 row. If `order_id` should be unique, retain one O106 record after verifying the duplication. Keep O105 for overall revenue but label its region as unknown for regional summaries. Record both choices.

## Practice

Find the data-quality issues and state how each affects a channel summary and a regional summary.

## Learner submission

O106 appears twice, so I would remove one copy. O105 has no region, so I would delete it.

## Feedback

The duplicate rule is reasonable after confirming grain. Deleting O105 would understate store revenue. Keep it for channel totals and use an Unknown region for regional analysis.

## Adaptation

Recalculate summaries with one O106 and O105 retained.
