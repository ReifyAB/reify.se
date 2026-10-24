---
title: "activerecord-pg-format-db-structure: tidying up Rails' structure.sql"
tagline: "RubyGem"
description: "Tidies up Rails' structure.sql after every migration, using a real SQL parser instead of regexps."
tags: [open-source, ruby, rails, postgresql]
---

If your Rails app uses PostgreSQL and `structure.sql`, you have probably seen noisy diffs between coworkers' machines after a migration. activerecord-pg-format-db-structure hooks into `rake db:migrate` and rewrites the file into a compact, consistent form. It parses the SQL with [pg_query](https://github.com/pganalyze/pg_query) and transforms the AST, rather than doing search and replace with regexps. I first released it in January, and version 0.6.1 is out today.

By default it will:

- inline primary keys, serials and table constraints into the `CREATE TABLE`
- move indexes right below their table
- group `ALTER TABLE` statements into one per table
- sort table columns and the `schema_migrations` inserts
- format and indent the whole file consistently

Each transform can be switched on or off, and you can add your own. It's on RubyGems, so setup is one line in your Gemfile:

```ruby
gem 'activerecord-pg-format-db-structure'
```

It was inspired by Lukas Fittl's [activerecord-clean-db-structure](https://github.com/lfittl/activerecord-clean-db-structure).

Source on GitHub: [ReifyAB/activerecord-pg-format-db-structure](https://github.com/ReifyAB/activerecord-pg-format-db-structure)
