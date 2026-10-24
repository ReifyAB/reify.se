---
category: engineering
title: "Pair Programming in the Cloud"
tagline: "PugglePay dev blog"
description: "How we keep pair programming when one of us is abroad, after trying screen sharing: AWS, SSH, tmux and Emacs."
tags: [emacs, tmux, remote, pair-programming, screen-sharing]
---
At PugglePay, we like to program in pairs. When everyone is working in
the same office, that's pretty easy: we just share a computer, and use
whatever text editor the owner of the computer has (in our case
Emacs, Vim or Sublime Text 2).

But things get complicated when one of the developper decides to move
abroad for a couple of months...

<!-- more -->

## First attempt: No Pair Programming

Well, the easiest solution is simply to stop pair programming and
simply review each other's code. But we observed that it's really more
difficult to solve problems in a simple and elegant way while
programming on your own. One is also more reluctant to fix broken
windows on code that is already written.

So I guess that's not a viable solution. Pair programming is great,
and passing on it simply because we are not in the same place is just
too sad.

### Pros:

- Trivial to setup

### Cons:

- Makes me a sad panda

## Second attempt: Screen Sharing

The simple approach is to simply run some sort of screen
sharing application. We have been using
[Screen Hero](http://screenhero.com/), which is really awesome. Each
user that joins a Screen Hero session gets his own cursor with his
name on it. In addition to that, we run google hangouts or Skype to
talk to each other.

This works great, except that there is some lag for the users that are
not hosting the session, and the quality of the video is not perfect.
Spending most of the day writting code with an image full of
compression artifact, even minors, is pretty painfull.

Also, since we recently migrated to JRuby, some of us still use a
not so powerful MacBook Air, running Skype + Screen Hero + Spork +
Nailgun + Chrome made our computers really, REALLY slow.

So that didn't work for us, but if you have access to a really good
internet connection and powerfull computers, this might be the best
solution.

### Pros:
 - Easy to setup
 - Fancy cursors for everyone

### Cons:
 - Slow
 - Compression artifacts

## Third attempt: AWS + SSH + tmux + Emacs

Inspired by other remote-working companies like
[Relevance](http://thinkrelevance.com/), we decided to try a
combination of SSH, tmux and Emacs. To make things easier, we decided
to setup all that on a High CPU Amazon EC2 instance.

To share sessions with [tmux](http://tmux.sourceforge.net/), we use
[wemux](https://github.com/zolrath/wemux), which is a small wrapper
around tmux to simplify multi-user sessions.

I order to work with git, we simply need to active Agent Forwarding
when we ssh in to the instance. It's also interesting to setup some
port forwarding when we want to run `rails server`.

To do that automatically, we just configured a host in our local
`~/.ssh/config` that look something like that:

```
ServerAliveInterval 60

Host pp
  HostName pair-programming.pugglepay.net.
  User pair
  ForwardAgent yes
  LocalForward 3000 127.0.0.1:3000

```

And then we just have to `ssh pp` to access the instance.

We met some problem when running Emacs from the terminal, since the
meta key (the `cmd` button on mac) is not properly interpreted. Also,
`C-<left>` and `C-<right>` were not properly recognized.

[iTerm 2](http://www.iterm2.com/#/section/home) solved the first
problem. In the preference panel, under Profiles/Keys, select "Left
otion key acts as +Esc". Now we can use the `alt` key as the meta key.

We solved the second problem within emacs, by mapping the ASCII escape
sequence received from `C-<direction>` to `C-<direction>`. That's what
we added to our `~/.emacs/init.el` file:

```
(global-set-key (kbd "M-[ c") (kbd "C-<right>"))
(global-set-key (kbd "M-[ d") (kbd "C-<left>"))
(global-set-key (kbd "M-[ a") (kbd "C-<up>"))
(global-set-key (kbd "M-[ b") (kbd "C-<down>"))
```

This solution is pretty nice, but it restricts us to Emacs, vim, or
editors that can be run in a terminal. It also requires a lot of
effort to setup. We also get the super annoying scrolling with tmux
( `C-b [`, is there a better way?).

It might have been easier to setup tmux with vim instead, but we have
a much more efficient workflow with emacs at the moment.

Though a nice side-effect of developping on the exact same type of
instance that we deploy our application to is that we find bugs that
we might have missed while developping on our local machines. We found
a bunch of timezone-related bugs for instance.

The plus side is that once everything is in place, it's really
comfortable to program. We share the same cursor, the same window,
there is not compression artifacts, and all is super fast.


This is clearly the best solution we have found so far. Plus it's a
really geeky one, and we get to learn tmux along the way.

### Pros:
 - Fast
 - Convinient
 - Geeky

### Cons:
 - A lot of configuration
 - No support for sublime text 2
 - Weird scrolling with tmux

## Conclusion

We're still kind of green in the field of remote pair programming, but
we found a pretty good solution for now. There is clearly room for
improvement, but remote pair programming feels pretty much like local
pair programming (even arguably better).
