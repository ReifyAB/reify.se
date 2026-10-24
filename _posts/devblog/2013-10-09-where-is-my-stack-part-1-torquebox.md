---
category: engineering
title: "Where is my stack? (Part 1): Goodbye Torquebox"
tagline: "PugglePay dev blog"
description: "After five months in production we said goodbye to TorqueBox, and went the Unix way: Nginx, Passenger, Resque and Monit."
tags: [torquebox, jvm, jruby, sysadmin, scheduling]
---
So this is how it ends.

This week was the last week we ran TorqueBox in production. We've had
it running in production for 5 months. That's something! We
switched to TorqueBox in the first place to avoid headache with system
administration. Sadly, There Ain't No Such Thing As A Free Lunch
(TANSTAAFL), and we traded our problems with new ones, namely JRuby
and the JVM.

<!-- more -->

## Previously on "PugglePay"

In an [earlier post](/blog/2013-05-03-torquebox-or-how-i-learned-to-stop-worrying-and-love-the-jvm), I discussed some problem we had with TorqueBox from the very
beginning, but that we thought could overcome:

- slower tests
- memory leaks
- no zero-downtime deploy

The only problem that was solved (and only recently) was the zero
downtime deploy. Other problems have appeared in the meantime:

- gem incompatibility
- shaky OpenSSL support
- very tricky setup with Spork
- assets pre-compile that take forever

## What to do?

Most of those problems are related to JRuby, and I'm confident that
they will be solved someday. Another thing to point out is that we
migrated a fairly large application, so it might be easier to spot
memory leaks when building an app from the ground up.

But for our case, we reached the conclusion that TorqueBox was not a
good fit given our current needs, and went therefore the other way.

And that meant the Unix way.

Instead of adding the one big component, we've had to add a bunch of
smaller ones. We are now using Nginx+Passenger Enterprise as web-server,
Redis+Resque+resque_scheduler for cluster-wise scheduling, and Monit for
keeping all those services running.

So we did not want to become full-blown sysadmin, but that became the
only viable option for us.

We were only treating the symptom though, and not the decease: we did
not want to become Sysadmins because the tooling we've been using for
system administration were so painful to use.

So that's how it all began: with looking for a replacement for our
own mixture of ruby scripts and Chef recipes...

## On the next episode of PugglePay Development

The team learns new encryption techniques ("We should totally use
GPG!"), discover new tools ("Ansible all the things!") and write some
libraries ("Mr. F~~").
