---
category: engineering
title: "Docker on Mac OSX in 2016"
tagline: "Zimpler dev blog"
description: "Is Docker on Mac ready for development? Mostly yes, and it looks like it'll soon be great."
tags: [docker, macosx, ops]
---
TL;DR: Docker on Mac is viable and seems like it'll soon be great.

<!-- more -->

## Why Docker?

When hiring a new developer at Zimpler, we aim at making them deploy
something to production on their first day. That means we need to be
able to setup a Dev machine with all its dependencies within half a
day while allowing that person to work in an environment they are
familiar with (Operating System, Text Editor...).

In order to achieve that, we currently use Vagrant images for each
project to minimize the global dependencies on our computers while
keeping a uniform Dev environment close to our production setup.

This allows us to take any laptop from zero to ready to commit within
a couple of hours.

This works great with a few downsides:

* Memory footprint

* File System Events propagation inside the machine (for things like auto-tests)

* Clunky to setup, provision and share images.

As an alternative, we've been looking at using docker for our Dev
environment. Our product team (developers and designers) are using
both Mac and Linux machines, therefor making this work flawlessly on
both was a requirement.

## First attempt: Docker for Mac

So we got started, and went straight to trying Docker for Mac
([https://docs.docker.com/docker-for-mac/]()). With just a brew install,
it works! Out of the box. That's super nice!

Sadly, there is one major issue: the current implementation of the
docker File System abstraction `osxfs` used by Docker for Mac is slow
and CPU intensive. Really badly slow. On one of our projects (with
about 30k lines of code that need to listen to file changes), the
compile time went from 2 seconds on our Vagrant setup with shared NFS
volume to 1 minute (!) in docker.

There is a performance bug reported on their bug tracker
([https://github.com/docker/for-mac/issues/77]()), and apparently work
is underway to improve this. Hopefully, we can return to Docker for
Mac in a few month.

Note that this is probably not an issue for everyone: perhaps
performance on smaller projects or requiring less file system IO is
acceptable. I would recommend trying that approach first.

### Verdict: Docker for Mac

Pros:

* Works out of the box

* Minimal dependencies and setup

Cons:

* unusably slow file system for our case

## Second attempt: Docker Machine through Dinghy

We were not about to give up so easily, especially since the previous
attempt took us a total of 10 minutes (really looking forward to it
being usable!).

So the next attempt was to try to run a docker machine with a mounted
NFS volume (we knew that performances of sharing a volume between a VM
and the host to be good).

After some research, we thought the best approach would be to use
dinghy ([https://github.com/codekitchen/dinghy]()).

That was fairly easy to setup (a simple brew install away), although
it is not as transparent as Docker for Mac and requires VirtualBox as
an extra dependency.

Well, turns out that works very well, and we managed to get things
working in an afternoon on one of our ClojureScript project.

But then, we tried to dockerize one of Rails projects, where we use
private gems stored on Github. And in order to install the
dependencies needed by the app, we had to get SSH agent forwarding
working inside the container.

Sad face: because of dinghy, this is actually quite hard because we
need to first forward the SSH agent to the docker-machine VM, then
mount the SSH agent socket from the VM to the container as a volume.

So the way we solved that is to write a custom `dinghy-connect` helper
that makes sure the docker-machine is running and that SSH forwarding
from the host to the docker machine is setup, then exports an
environment variable to the path of the SSH agent socket inside the
VM.

The end result can be seen in that gist:

[https://gist.github.com/Jell/546244f4fcb6b4596d3f66386e0d8102]()

After using this setup for a week, it feels actually quite nice! And
when compared to our previous setup with Vagrant, even including the
needed SSH-forwarding "hack", it's on par for Mac usage.

### Verdict

Pros:

* it works!

Cons:

* More dependencies

* hack needed for SSH-forwarding

## Conclusion

Docker for Mac looks super promising. When the performance problems
are fixed, it's going to be an excellent experience. For now, using
docker-machine through dinghy with some manual patching is still quite
good.

I will personally be using Docker for my Dev environment for the
foreseeable future.
