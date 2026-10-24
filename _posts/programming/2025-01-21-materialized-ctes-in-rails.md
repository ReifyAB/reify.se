---
category: programming
title: "Materialized CTEs in Rails"
tagline: "Rails pull request"
description: "Adding .as_cte, so ActiveRecord's .with can build MATERIALIZED and NOT MATERIALIZED CTEs."
tags: [open-source, ruby, rails, postgresql]
---

Since Rails 7.1, ActiveRecord can build Common Table Expressions with `.with`. What it can't do yet
is add a `MATERIALIZED` (or `NOT MATERIALIZED`) hint, which I needed in one of my Rails applications.

<!-- more -->

In PostgreSQL, that hint decides whether the CTE is computed once on its own, or inlined into the
main query for the planner to optimise as a whole. Most of the time inlining is what you want, but
when the planner picks a bad path, materializing the CTE is a simple way to steer it.

Arel's `Cte` node already supports the hint; ActiveRecord just never builds one. So I've opened a
[pull request](https://github.com/rails/rails/pull/54322) that does it in three small steps:

1. build CTEs with `Arel::Nodes::Cte` instead of `Arel::Nodes::TableAlias`;
2. let `.with` accept a `Cte` node directly;
3. add a `.as_cte` query method to turn a relation into one.

```ruby
Post.with(
  Post.where("comments_count > ?", 0).as_cte(:posts_with_comments, materialized: true)
)
# => ActiveRecord::Relation
# WITH "posts_with_comments" AS MATERIALIZED (
#   SELECT "posts".* FROM "posts" WHERE (comments_count > 0)
# )
# SELECT "posts".* FROM "posts"
```

`materialized: false` gives you `AS NOT MATERIALIZED`, leaving it out keeps today's behaviour, and
it works with `.with_recursive` too.

I was nudged into opening it from the discussion on an
[earlier pull request](https://github.com/rails/rails/pull/48305#issuecomment-2605521114). Now
let's see what the Rails team thinks!
