---
category: programming
title: "ClojureScript: from zero to production (Part 1)"
tagline: "PugglePay dev blog"
description: "What we learned shipping our first user-facing ClojureScript app, starting from scratch."
tags: [clojurescript, clojure]
---
A few weeks ago, we've released our first user-facing ClojureScript
app. We developed it over the course of couple of months, starting
from scratch.

We had previously launched a couple of non-critical Clojure apps (our
slack bot, some testing tools), most of our projects being written in
Ruby.

<!-- more -->

## Motivation

PugglePay is a payment company, and we wanted to provide a page for
our users to see their unpaid bills and get an overview of the last
few transactions.

After investigating our options, we decided that we should start a new
separate project that access all relevant info from our backend via an
API, then present it to the user in a nicely structured way.

We've also decided that we did not want to have a user account and a
system of login, instead access to the page should be through one-time
links sent to the user along with each payment information.

We therefore realised that we could have this app as a single-page
JavaScript app. JavaScript
[sucks](https://www.destroyallsoftware.com/talks/wat), so we wanted
to find a better way to build client-rich apps. Therefore ClojureScript.

We chose ClojureScript because we knew the semantics of Clojure were
very good, and given our knowledge and experience, this was the best
fit.

## Our current setup

Our stack consists of the following libraries:

 - [figwheel](https://github.com/bhauman/lein-figwheel)
 - [reagent](https://github.com/reagent-project/reagent) (and therefore react)
 - [re-frame](https://github.com/Day8/re-frame) (most epic README ever btw)
 - [kioo](https://github.com/ckirkendall/kioo)
 - [speclj](http://speclj.com/)

[Figwheel](https://github.com/bhauman/lein-figwheel) is I think the
key to the success of this app. It's trivial to setup, and you get
interactive development without any particular editor support.

This is very important, compared to the usual REPL-driven development
of Clojure projects. This means that beginners can get started without
having to setup anything, and focus on the code before focusing on
setting up their environment.

I believe the second important factor was using
[Kioo](https://github.com/ckirkendall/kioo). Because the templates are
made of pure HTML and are rendered using composable transformations,
developers and designers were able to work in parallel without
interfering with each other and communicating using HTML as
lingua-franca.

This made the development very smooth.

One weak point was testing setup, which ended up being a bit too much
of a hassle to setup. New tools are now surfacing that would make
things smoother in the future
([devcards](https://github.com/bhauman/devcards) maybe?).

## Lessons learned

I'll just list a few here, more to come in later posts.

### DOM manipulation is slow, React is awesome

In the first version of our app, we used
[enfocus](https://github.com/ckirkendall/enfocus) instead of
[kioo](https://github.com/ckirkendall/kioo), and did not use React at
all. This made the app much too slow when testing on the IPhone, so we
re-wrote it using react.

Fortunatelly, we had already structured the app around a single atom
holding all our state, so this was an easy transition.

### The iphone 4 javascript engine is utterly broken

We tracked down an incredible bug when using hashing functions that
only happened on iphone 4 when NOT using a web inspector.  You can
read about it here:
[http://dev.clojure.org/jira/browse/CLJS-1380](http://dev.clojure.org/jira/browse/CLJS-1380)

TL;DR: the JIT compiler has broken inlining of bit operations on the
iPhone 4 (note: not on the iphone 4S! only specifically using the
hardware version of the iphone 4). The solution: use `try ... catch`
to disable JIT compiling for functions doing bit operations.

Separate blog post coming soon!

### re-frame is good

Once you get around to it, it's a very small library that will help
you organize the flow of your app. We started without, and all-in-all
it was not bad, except for the part where we had to deal with side
effects or query the app state in different in different ways and
places.

But still ended up with a structure that was very similar to re-frame,
except less good, and adhering to the re-frame conventions helped us
better structure everything with a linear flow of data.

Separate blog post coming soon!

### tracking errors is not a bad idea

We use [Honeybadger](https://app.honeybadger.io/) to track errors on
the page (that's what we were using for our Rails app to begin
with). We were afraid it would end up being very noisy, but we
actually get only very few errors related to loading issues (and we
plan to fix those).

### Write integration specs in Clojure

The way we write integrations tests is to have a setup phase in our
specs where we compile our app from withing Clojure using
`cljs.build.api/build`, start a compojure / jetty server that serves
the app and stubs the API the app talks to, and run the specs using
`clj-webdriver` and phantomjs.

Separate blog post coming soon!

## Conclusion

We have been live for a few weeks now, and everything runs
smoothly. Everybody at the office has contributed to the project, have
a good understanding of its inner workings, and is satisfied with the
result. All in all, a pretty good experience.
