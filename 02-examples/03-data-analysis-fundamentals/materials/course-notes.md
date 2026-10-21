# Data Analysis Fundamentals — Example Course Notes

## Table structure

A row represents one observation at a declared grain. A column represents one variable. Data types determine valid operations: numbers can be aggregated, dates can be ordered, and categories can be grouped.

## Questions and measures

Start with a decision question. A metric is a quantity to calculate; a dimension is a category used to split or filter it. Define both before calculating.

## Cleaning

Check missing values, duplicates, inconsistent labels, impossible values, and unexpected types. Do not silently delete records; document the rule and its consequence.

## Summaries

Filtering narrows the rows. Grouping partitions rows by a dimension. Aggregation then produces a result such as count, sum, or average for each group.

## Distribution

The mean uses every value and can be pulled by outliers. The median is the middle ordered value and is often more robust. Always inspect count and spread before treating one number as typical.
