---
category: engineering
title: "From Sidekiq to Solid Queue"
tagline: "At Dockspot"
description: "Why we moved our Rails background jobs from Sidekiq to Solid Queue, and how we did it one worker at a time."
tags: [rails, solid-queue, activejob, sidekiq, postgresql]
---

This week we removed Sidekiq and Redis from Dockspot. Our background jobs now all run on Solid
Queue, backed by the same Postgres database as the rest of the app.

<!-- more -->

## Why

Two guarantees we didn't have with Sidekiq.

The first is a **transactional outbox**. Solid Queue keeps its jobs in the same database as our
models, so enqueuing a job is part of the same transaction as the rest of the work: a job only
exists if the transaction commits. No more jobs pointing at records
that were rolled back, and no more committed changes whose follow-up job never got queued.

The second is **at-least-once delivery**. Sidekiq takes a job off Redis when a worker picks it up, so if
the process dies mid-job (say, killed for running out of memory), that job is gone. Sidekiq's own
[docs](https://github.com/sidekiq/sidekiq/wiki/Reliability){:target="_blank"} are upfront about it:
Sidekiq "does its best to never lose jobs but it can't guarantee it". Reliable fetch is a Sidekiq
Pro feature. Solid Queue keeps a claimed job in the database until it's done, and if a worker dies
mid-job, the job is marked as failed: it stays there for us to inspect and retry, instead of
disappearing.

Moving to ActiveJob was a nice upgrade on its own, too: named arguments, and passing Active Record
objects directly instead of an ID we'd then look up again inside the job.

## How

We set up Solid Queue next to Sidekiq at the very end of 2024, with Mission Control to look at the
jobs, and migrated the simplest and least impactful job first to try the setup out. A few things showed up early:

- finished jobs aren't cleaned up automatically, so we added a recurring job for that;
- the worker used a lot of memory, and starting it with the rake task instead of `bin/jobs`
  seemed to help;
- ActiveJob doesn't retry failed jobs by default, so every job that should be retried needs to say so.

This summer we moved the rest of the Sidekiq workers over, one domain at a time. We renamed each one along the way to a consistent
`Domain::DoSomethingJob`. The last step was the jobs we ran from Heroku Scheduler, which became
recurring jobs in Solid Queue. After that, nothing used Sidekiq or Redis anymore, and we removed both.
