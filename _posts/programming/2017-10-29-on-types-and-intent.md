---
layout: post
category : programming
tagline: "how much can we communicate using types?"
tags : [types,programming]
---

I love Clojure and I love Haskell. Those are two of my favourite
languages (I also really love Idris). They both offer semantics with
very interesting properties and trade-offs.

Sadly there is a disconnect between the communities in both of those
languages, where people try to communicate what they like about their
favourite language but tend to do that by contrasting it with other
languages, and that ends up being quite antagonistic and put people on
the defensive.

<!-- more -->

This is as true of people saying static typing is useless as it is of
people saying that dynamically typed languages are recklessly
unsafe. It would make life so much easier if either of those statement
were true, but sadly we have to deal with the usual grey area.

We also have to acknowledge that we are nowhere near the end of our
journey towards understanding information and computation, we don't
even understand our own reality how can we presume knowing how to
model it using computers?

Instead of figthing, we should strive together to find a deeper
understanding of the principles and trade-off that are involved when
writting and evolving code. I would like to make such attempt today by
opening a conversation on the communicative power of types.

# What's in a type?

Types are great! They can carry a lot of information if you know what
to look for. Let's look at: `foo :: [a] -> [a]`. In Haskell, this type
says "this is a function from List of `a` to List of `a`". But this tells
us so much more than that:

* We have no assumptions on `a`, so we know we're not transforming the elements of the list.
* Since the only assumption we have on the input is it's a list, that's the only thing we're allowed to manipulate. So we can only change its length, ordering and repetitions.
* Since there is no `IO` in the type, the author is communicating that we can assume this function has no side effects.

So there really is not that many functions that satisfies this type. Sadly, there is still an infinity of them:

```haskell
foo1 :: [a] -> [a]
foo1 x = []

foo2 :: [a] -> [a]
foo2 = tail

foo3 :: [a] -> [a]
foo3 = reverse

foo4 :: [a] -> [a]
foo4 = cycle

foo5 :: [a] -> [a]
foo5 = init

foo6 :: [a] -> [a]
foo6 [] = []
foo6 (x : xs) = foo xs ++ [x] ++ foo xs

foo7 :: [a] -> [a]
foo7 [] = []
foo7 xs@(x : _) = take (length xs) $ repeat x
```

You get the idea. The types themselves do not communicate all the
intent, but they do provide some extra knowledge. I think from the
above examples we can agree that intent has to be communicated through
some other way (meaningful function names and documentation).

Let's look at `foo7`:

```haskell
foo7 [1,2,3]
-- [1,1,1]
```

Is the information "we're not transforming the elements of the list"
useful here? In this particular context, not really, even though the
shape of the list is the same, its value is very much different. They
also have very different runtime properties (one of them even being
infinitly recursive).

There's another thing: in this case, the implementation is still
very much concrete on the type `List`. If we want to use sets or
vectors instead, we have to work at another layer of abstraction. In
Haskell, that would be Monoid:

```haskell
import Data.Monoid

foo8 :: Monoid a => a -> a
foo8 x = mempty

foo9 :: Monoid a => a -> a
foo9 x = x <> x

foo10 :: Monoid a => a -> a
foo10 x = x <> x <> x
```

We have even fewer assumptions on the input, that's awesome! However,
now that we're at a higher level of abstraction, the sentence "foo
takes as input types that have an instance of the Monoid typeclass and
returns values of the same type" both carries more and less information.

`Monoid a` means the type `a` contains a value that's considered the
empty element (mempty in Haskell), and an operation on its values
(mappend) that can combine them into a value that belongs to that also
is of type `a`. They should follow a few special rules (appending the
empty value should not change the result for instance), but those
rules are not enforced in Haskell, so it does not exactly help our
understanding just by looking at the type.

This is an intersting bit of trade-off: **the higher abstraction you use**
(and therefore the fewer assumptions you make), the more general you
make your code and **the more difficult it is to reason about it without
context**.

For instance, did you know that functions with monoidal output also
form a monoid? So this works:

```haskell
foo10 (++) [1] [2]
-- [1,2,1,2,1,2]
```

Also did you know that you can you can form a monoid using numbers?
You can have more than one even: the value `0` and addition form a
monoid (Sum), and so does the value `1` and multiplication (Product).

So at the REPL, I can ask the type of this expression and it works:

```haskell
:t foo10 (+) 1 2
-- (foo10 (+) 1 2) :: (Num a, Monoid a) => a
```

However, because there is more than one possibility for `a` to be a
number and form a monoid, Haskell cannot know which one you mean from
the type alone (even though it should be obvious from the value `+`
that we mean the Sum definition). So without more hint, Haskell will
not be able to understand what we mean and refuse to compile:

```haskell
(foo10 (+) 1 2)

<interactive>:82:1: error:
    • Ambiguous type variable ‘a0’ arising from a use of ‘print’
      prevents the constraint ‘(Show a0)’ from being solved.
      Probable fix: use a type annotation to specify what ‘a0’ should be.
      These potential instances exist:
        instance Show All -- Defined in ‘Data.Monoid’
        instance forall k (f :: k -> *) (a :: k).
                 Show (f a) =>
                 Show (Alt f a)
          -- Defined in ‘Data.Monoid’
        instance Show Any -- Defined in ‘Data.Monoid’
        ...plus 30 others
        ...plus 54 instances involving out-of-scope types
        (use -fprint-potential-instances to see them all)
    • In a stmt of an interactive GHCi command: print it
```

So we need to explicitely tell Haskell that we mean the Sum version:

```haskell
(foo10 (+) 1 2) :: Sum Int
--Sum {getSum = 9}
```

So it's really cool that we're able to express our code in a way
that's at the highest level of abstraction because then we can apply
this code in any context that satisfies this abstraction, which is
also the downside of it, because then you cannot know in which context
that function will be used.

Let's compare that to a piece of Clojure code:

```clojure
(reduce + [1 2 3])
;;=> 6

(reduce + [])
;;=> 0

(reduce * [])
;;=> 1
```

How does that even work? Clojure manages to take advantage of the
monoidal properties of `+` and `*` over numbers because that knowledge
is found at the value level and not at the type level, so there is no
ambiguity in the result. The downside is that you can't know
beforehand if the reducer is monoidal or not, so you get a runtime
error here instead:

```clojure
(reduce - [])
;;!! ArityException Wrong number of args (0) passed to: core/-
```

Ah! Fun fact: the empty element for a monoid is implemented as the
zero arity for a function. This is purely conventional. Obviously
that's also not general: it means a given function can only be
monoidal in one domain (numbers in the case of addition and
multiplication).

That doesn't mean we're stuck, we just have to use the fact that `-`
forms a Semigroup on numbers instead (Monoid without neutral element),
so that means we need to pass the initial value explicitely:

```clojure
(reduce - 0 [])
;;-> 0

(reduce - 0 [1 2 3])
;;-> 6
```

The trade-off here is: **I can think about those things** in
category-theory terms, and **I don't have to impose this thinking on
people around me** (and in particular beginners). But the downside is
**I'm not helped by the language** out of the box to follow those
rules.

To me that's some interesting trade-off to think about!

# On the no-side effect convention

Maybe this will come as a shocker, but Haskell IO is pure by
convention. This convention is enforced to some extent by the type
system, but you can always bypass it and do weird stuff. Let's define
this interesting piece of code:

```haskell
import System.IO.Unsafe

foo11 :: Int
foo11 = unsafePerformIO $ do
          print "yo"
          return 11
```

If we call it, it will print `"yo"` then return 11 the first time
around, and the second time will only return 11 and not print
anything.

```haskell
foo11
--~ "yo"
-- 11

foo11
-- 11
```

Mind you, this is not a bad thing! Having side-effects internally does
not necessary mean having visible side-effects globally. Memoization
for instance is a useful "side-effect", Haskell does that as a runtime
optimisation (like we see with `foo11`). Or transient datastructures
can me mutated in place to speed things up within the context of a
pure function that returns the immutable version of that
datastructure, and it makes sense because performance is important.

You might say "Ha! but you're importing `System.IO.Unsafe` so we know
you're doing funky stuff!", and you'd be right: if you look at the
code, you get more info about its behaviour. But we're only interested
at **how much information the type annotations contain, not the code**.

Clojure chooses to be immutable by default, but does not try to
completely isolate side-effects. However it would not be fair to
consider all Clojure code to be as if implicetely inside an
`unsafePerformIO`!

Why is that? Because Haskell relies on the knowledge that a function
is pure to perform all sorts of optimisations. Like in our code above,
it chooses to memoize the execution of `foo11` because its type
signature says it's pure. This behaviour is implicit and happens
at the compiler level. You'd have to express that explicitely in Clojure:

```clojure
(def foo11
  (memoize
   (fn []
    (println "yo")
    11)))
```

Given there is no built-in type annotation in Clojure, what am I
getting at? Well the "type" information is implicit, and much weaker
than with Haskell, but the convention is stronger than other languages
that are not immutable by default. You can most of the time assume the
inputs are immutable, and are either a value or a collection of
values.

"Most of the time", "assume"... This doesn't sound very safe does it?
The thing is, even though it's not obvious, we have to "assume" and
"most of the time" in Haskell as well. We have to assume that the
implementation of Monoid follows its associative and neutral element
laws, and that our code does not contain non-lazy infinite
recursions... At best, we can verify them through testing. Of course
this is not true with dependent typing and Idris, but even with the
state of the art you always end up drawing a line somewhere in
practice.

The interesting question (to me) is: **how much should we assume and
how often?** Where do you draw the line for a given context?

# Convention dominates information

This is what I'm getting at with this conversation.

There's a point where **convention dominates information**, otherwise
you get to an infinitely high level of abstraction in turn requiring
an infinite amount of context.

Where this point lies is the core of the debate. My position is that
the conventions enforced statically at the type level by languages
like Haskell are not necessary nor sufficient and come at a non-zero
cost. Whether that cost is higher than the value provided is
debatable, but the fact that it comes at a cost should not be
controversial. Understanding the cost / value proposition of static
typing is really important to me.

You can look at the fact that Ruby on Rails has been such a success
and come to the conclusion that this success was only due to some Pop
Culture effect or random chance. But what it did was provide a set of
conventions that were super efficient and was able to communicate
those conventions somehow, thus pushing the industry forward.

# On means of communication

Here are some of the means to communicate intent when writting code:

* function and argument names
* documentation
* type and contract annotations
* the code itself

If we look purely at the communicative power of what we write, the
code itself is it: it's literally the definition of what we
mean. However, it's not convenient to read code, so the question is
what do we use to make our life easier and our understanding quicker?

The answer is dependent on the abstractions available in the language
we use: **how many particular cases do we need to keep in mind at all
time?**

Haskell has the following approach: there is an infinite amount of
abstractions that are expressible in the type system so that you don't
have to keep track of all of them in your head.

Clojure has the following approach: there is a very small amount of
abstractions, so that you can keep all of them in your head.

Those two approaches require two different kinds of communication. If
you have a very small set of abstractions, you can easily keep all of
them in your head and apply them in your understanding of your
code. If you have an infinite amount of abstractions, then you want as
much help from the language as you can to not have to juggle all of
them in your head, and type information becomes paramount. But beware
that this can be a self-fulfilling profecy: **you need an infinite
amount of types to deal with infinite abstractions, and infinte
abstractions require an infinite number of types**.

So the end of the Haskell (PureScript, Idris...) journey is an
asymptotic one: values and types evolve towards a meta-circular answer
that's extremely close to the essence of mathematics and
phylosophy. It's an awesome journey by the way, I personally needed to
step into the realm of dependent typing to begin to get an intuition
about this.

I digress a bit: my point is that **if your goal is infinite abstraction,
your solution will require infinite communication**.

But infinite abstraction and infinite reuse is not one of my personal
goal. What I care about is producing things as fast and reliably as I
can, and the 80/20 pareto rule is my guide in any decision I make.

As an engineer, if my solution is perfect then I wasted too many
resources in making it perfect. I want to find the most cost-efficient
way to implement something.

# How much can I sacrifice to reach my goal?

What's the minimum I need to communicate my intent and get it out
there? Code.

This is my personal preference and not everyone might agree with this
priority, but if there is a case where I want to move as fast as
possible, I want to be able to take risks and try to get it out
there. Sometimes, if there is a 1 out of 10 chance of succeeding, I
want to take that chance, and that might mean sacrificing all other
benefits for short term gain.

Sometimes being forced to think of all the edge-cases upfront is
exactly what I need: when implementing a protocol or a parser or
things like that, I want all the help I can with dealing with a
million abstractions, because those abstractions are pushed onto
me. So I'm not being dismissive of that use case.

But (most of the time) I want to work with a very small set of
abstraction and just make the simplest thing that can possibly work
without thinking about any of the edge cases. I might get a runtime
error, but the code will work 90% of the time and that will be good
enough for me to sell my product, adapt to a new market, who knows.

Having a type system that forces me to think about those edge cases
works against this stated goal. It forces me to be correct above all,
but this is not what I want: I want to have the happy path solved as
fast as possible, and I'll handle the edge cases as they show up
over time.

I also want the ability to add all those niceties and guarantees
to my code, but I want the freedom to take risks.

# How do I communicate intent?

The first step to good communication is finding meaningful names.

This is very much necessary anyway because the first step of
implementing something is understanding the domain of that thing, and
understanding the domain is all about naming things.

Same with documentation: documentation is part of understanding the
domain itself, and has value beyond the understanding of the code.

Also finding some examples, that really helps with
understanding. Those examples can be written as tests so that they can
allow you to verify your code.

Verification is a nice tool: it does not guarantee anything, but it
allows you to check some of your assumptions. And you do need to
verify your code, and that means writting tests.

Finally, type and contract annotation help with the boundaries of your
code. Those allow to not only communicate the API between your
functions, but also make sure that information is kept in sync with
the code.

All of the above require constant maintenance. You might believe none
of them should be negociable, but I believe they all are: for your
given domain, you have to establish the cost and value of each of
those, and decide if you want to invest in them upfront or only after
you're successful.

In some cases, the code itself is not even the most important, and the
documentation and types are everything! And sometimes, only the
artefact you've created matters.

# What do I care about right after "it works"?

Beyond communicating intent, verifying and proving things, there are
many other considerations I have in mind:

* Will it run fast enough?
* Will it scale?
* Will it run out of memory?
* Am I using the right datastructure?

And so many other considerations. In my experience, those answers are
easier to find in a language with a clear set of datastructure and a
list of functions on those datastructure that have consistent runtime
properties.

It is also much easier in a language that does not abstract over its
runtime.

It is not impossible to express and have guarantees about those
properties in a type system. In fact, Linear types have just been
added to the Haskell compiler to communicate some of those. And it's
super neat! I love that. It's just that you NEED those in order to get
an understanding of runtime properties when running at this level of
abstraction, because otherwise you simply can't wrap your head around
it.

Look I love those! I really really enjoy this, and I know this, but as
an engineer I want to be able to make sacrifices and trade-offs to get
imperfect solutions out, because imperfect solutions are the cheapest
to produce.

# Engineering and Science

We need Computer Science. But we also need Computer Engineering. We
need to understand what "the minimum requirement" for a solution is,
what constraints we can relax and what kind of risks we're taking.

We can't throw around terms like "correctness" or "freedom" without
understanding what they mean and their cost.

Too often the conversation ends up being "you don't like types because
you don't know enough types", or "types is only for academia and is
always standing in my way". But I hope we can find an place where
someone doesn't have to either prove they know Profunctor Optics or
avoid using precise mathematical terms before their approach to
software engineering is taken seriously.

# Disclaimer: what do I know about the subject?

Here is a bit of info about me. Those are some of the things I have
played with and have investigated the trade-offs of in the context of
functional programming. I'm sharing this list because I find the topic
fascinating and I like to understand trade-offs:

* parametric polymorphism (Haskell, PureScript) vs ad-hoc polymorphism (Clojure) vs subtyping (Clojure, OCaml)
* dynamic typing (Clojure) vs gradual typing (Racket, Clojure + core.typed) vs static typing (Haskell, PureScript, Elm)
* dependent typing (Haskell, Idris)
* verification (Promela) vs proof (Idris, Agda)

Those trade-offs include soundness, verification, proofs, inference
(type or code!), runtime properties, expressivity...

All those aspects and tools are super interesting and useful when
applied in the right context. But there is no general best solution or
programming language, because you need to define fitness in your
context first. Also I encourage you to explore all those axis and
more! But above all, please explore beyond the one axis you're
familiar with.

# Conclusion

I have a million more things to express, but the gist of what I'm
trying to say is: let's not conflate good software engineering
practices (or functional programming for that matter) with just static
typing, and let's not dismiss it either. Even static verification
should not be mistaken with or limited to static typing. Doing so goes
against the very essence of engineering. State your constraints,
assumptions and objectives first, and consider Static Typing as a
tool, not an end in itself.
