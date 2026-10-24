---
category: engineering
title: "From Heroku to Render"
tagline: "At Dockspot"
description: "Why we moved a Rails app from Heroku to Render, and what it took: images, deploys, rollbacks and backups."
tags: [rails, render, heroku, postgresql, devops]
---

Over the past few weeks we moved Dockspot, our Rails app for marinas and boaters, from Heroku to Render. The
move itself was the easy part. Most of the work was rebuilding what Heroku had been doing for us.

<!-- more -->

## Why

Two things made us start looking beyond Heroku. Last June, a
[major outage](https://www.heroku.com/blog/summary-of-june-10-outage/){:target="_blank"} disrupted
Heroku for most of a day, its status page included. Then in early February, Heroku
[announced](https://www.heroku.com/blog/an-update-on-heroku/){:target="_blank"} it was moving to a
"sustaining engineering model": stability, security and support, but no new features. A platform
in maintenance mode isn't one we wanted to keep building on, so we started trying out Render soon
after.

## The setup

Everything is declared in a Render Blueprint per environment: a Puma web service, a SolidQueue
worker, a small instance that only exists so we can open a Rails console, a nightly backup job, and
Metabase. We'd already [moved our background jobs from Sidekiq to Solid Queue](/blog/2025-08-20-from-sidekiq-to-solid-queue) last summer, so there was
no Redis to bring along: the worker just needs Postgres. The web, worker and console services all run the same Docker image of the app, built by GitHub Actions and pushed to GitHub's
container registry.

We build the image ourselves because if you let Render build from the repository, each service
builds its own copy of the app: there's no sharing builds across services. And there's nothing
like Heroku's "promote to production", where the exact build you tested on staging goes live. So
we build the image once ourselves, run it on every app service, and deploy and roll back with our own scripts.

The web service runs migrations in its pre-deploy step, and the other services wait for them before
starting:

```ruby
namespace :db do
  desc "Wait for all migrations to be applied"
  task wait_for_migrations: :environment do
    max_attempts = ENV.fetch("DB_WAIT_MAX_ATTEMPTS", 60).to_i
    interval = ENV.fetch("DB_WAIT_INTERVAL", 10).to_i

    puts "Waiting for migrations to complete..."

    max_attempts.times do |attempt|
      context = ActiveRecord::Base.connection_pool.migration_context
      pending_count = context.migrations_status.count { |status, _, _| status == "down" }
      if pending_count.zero?
        puts "All migrations applied!"
        exit 0
      else
        puts "Attempt #{attempt + 1}/#{max_attempts}: #{pending_count} pending migration(s), waiting #{interval}s..."
        sleep interval
      end
    end

    abort "Timed out waiting for migrations after #{max_attempts * interval}s"
  end
end
```

## What Heroku used to do for us

- **Deploy tracking.** On Heroku, a release webhook told Honeybadger about each deploy. Now it's the
  first step of the pre-deploy command, so if a migration fails we can see which deploy broke it.
- **Deploys and rollbacks.** This is our replacement for Heroku's promote. We dropped the production
  branch: a script promotes the image that is live on staging to production, and moves a
  `production` tag on the image in the registry. Rollbacks were the tedious part. The trick was to start from the digest of the image Render is running, not its
  tag, and work back to the commit from there.
- **Backups.** Heroku took our backups; now a nightly cron job runs `pg_dump`, encrypts the dump with
  each developer's GPG key and uploads it to S3. A small script restores the latest one into a throwaway
  Postgres container, so we know the backups actually work.
- **Dataclips.** Our saved SQL reports moved to Metabase.

Render also makes it easy to run PgHero next to the database, which found a missing constraint and a
few duplicate indexes.
