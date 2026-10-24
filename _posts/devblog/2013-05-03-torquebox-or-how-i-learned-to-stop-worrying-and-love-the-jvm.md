---
category: engineering
title: "Torquebox or: How I Learned to Stop Worrying and Love the JVM"
tagline: "PugglePay dev blog"
description: "Why we moved our Rails apps to TorqueBox on JRuby: messaging, daemons and scheduling without the sysadmin pain."
tags: [torquebox, jvm, jruby, sysadmin, messaging, daemons, scheduling]
---
So here is the thing. As a DevOp, SysAdmin is a PITA. Time spent
tweaking the servers to add such or such service is time not spent
actually producing value.

At PugglePay, we try to be agile and always look at the trade-offs
that are involved in every decision we make. So as we started
developing our product, we decided to go with the easy and fast track,
and that meant Amazon, Rails and MySQL.

Unfortunately, easy does not necessary mean simple, so we kept using
the same tools to the point where easy became complex. It was time
for us to do something difficult which was to use more tools and turn our
architecture simple again.

<!-- more -->

The difficult thing for us was to move out of our comfort zone because
our comfort zone was a dangerous place (remember the frog being slowly
boiled to death).

## Our problem:

- We needed queues. We kept on postponing using them because we wanted
  to Keep It Simple™, but simple meant using queues.

- We needed daemons. Stuff that run non stop, and that get updated
  after each deploy.

- We needed scheduled jobs. We used cron for that, but that meant
  the application and the server were tightly coupled. Not simple!
  (but easy)

If we look at all of the above, the easy solution would have been to
add a message processing lib like sidekiq, a short capistrano script
to redeploy our services and keep on using cron for recurring tasks.
But here comes the trick:

- We are going to need clustering. And we want all of the above to be
  clustered.

So as any good developer, we googled "rails queues cron clustering"
and found [TorqueBox](http://torquebox.org/).

## TorqueBox

The idea of TorqueBox is to add a layer of abstraction between the
server and your application. It's like you are building a city, and
TorqueBox offers to provide the sewer system, running water,
electricity and the Internet so that you can focus on the city
planning.

In practice, that meant webserver, messaging, recurring jobs, and
daemons out of the box, and the only SysAdmin we have to take care of
is to get TorqueBox running.

Wow. That looked exactly like what we needed. Only downside: it runs on
JRuby. Which means JVM. And we had zero knowledge.

But the concept was just too good to be so easily dismissed because of our
own lack of knowledge. It would be difficult for us, but it could
become easy on the long run.

## Investigation

So we started our investigation. The first step was to migrate our app
to JRuby. First downside: we got really slow tests. So that's the
first thing we had to improve.

The solution was to use [Spork](https://github.com/sporkrb/spork) and
NailGun. What we got are fast enough tests. It's slower than with MRI
(10% slower on average), but good enough.

So running on JRuby: check! Next step was to get the app running
locally on TorqueBox. Roughly, that meant:

``` sh
gem install torquebox
torquebox run
torquebox deploy
```

Boom. Trivial. Now let's deploy to Amazon. Well, there's a
[chef recipe](https://github.com/torquebox/chef-cookbooks). It
requires some extra work to get clustering going because Amazon does
not support multicasting (for automatic discovery of new nodes). Well,
clustering is for later, and for sure we're going to solve that
problem. So getting TorqueBox to run on Amazon: check!

Now let's deploy. Cool, there's a
[Capistrano recipe](https://rubygems.org/gems/torquebox-capistrano-support)!
We already used capistrano, so that was easy. Boom! Deploying to
TorqueBox: check!

Sweet! Now lets deploy again! Yay, it works! And again! Yay! And
again! Oups... Nothing works anymore. Well, we knew exactly nothing
about JRuby, the JVM or TorqueBox, so it took us a week to find out
that after a redeploy the connections to the database were only closed
after Garbage Collection, but garbage collection came too late in our
case.

So the solution was to add an `at_exit` hook that took care of closing
all connections after redeploy.

We also realized that we do not get zero-downtime deploy when
deploying to TorqueBox. That's sad, because we are going to need it in
the future. After googling a little more, we found out that this is a
feature coming with the next release. Fair enough.

So after a couple of weeks of research and testing, we were confident
enough that TorqueBox would make our system much easier to maintain in
the future, and decided that the pros were bigger than the cons.

So we took a leap of faith and deployed the whole thing in production.

## Running in production

It went pretty smoothly at first, but after a couple of deploy we got
a "PermGen out of memory" error. WTF is that?

Well, that's a story for another post. Long story short, closing the
DB connections was not enough because some references were being kept
that prevented the JRuby runtimes from being garbage collected after
each deploy. Also `jvisualvm` is an awesome tool that lets you inspect
a running JVM in realtime.

We have been running TorqueBox in production for a couple of weeks now,
and we are getting more familiar with it everyday. Our architecture is
much simpler, and the difficult bump we had to overcome is behind us.
So in the end, we believe that we have made the right choice.

But I think it is important to know that this was not a totally
painless migration. We had to learn about the JVM, how its garbage
collection works, which tool to use and which flags to set, while
making sure our development speed was not too much impacted by the
change. For us, it was worth it because we needed a better
infrastructure, and we did not want to rely on too many components.

## Conclusion

Pros > Cons, lots of new things to learn, but the end
result is a simpler architecture.

We'd love to share more of what we know, but we'd love even more to
acquire knowledge from others. So if you have some experience with
TorqueBox, please get in touch!
