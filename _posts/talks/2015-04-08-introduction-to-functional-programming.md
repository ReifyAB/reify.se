---
category: programming
title: "Introduction to Functional Programming"
tagline: "Got.clj meetup"
description: "A first tour of functional programming concepts, from values and pure functions to polymorphism, in Python, Clojure and Haskell."
tags: [talks, functional programming, python, haskell, clojure]
---

Tonight's Got.clj session was an introduction to functional programming. I built up the vocabulary step by step: values, expressions, evaluation, side effects, and why Clojure and Haskell only have expressions while Python also has statements. Each idea comes with examples side by side in Python, Clojure and Haskell.

What we went through:

- functions, arity, and routines versus functions
- pure functions, immutability and referential transparency
- higher-order functions, partial application and currying
- map, filter, reduce, list comprehensions, recursion, pattern matching and composition
- types as sets of values, and ad hoc, subtyping and parametric polymorphism

```haskell
twice = (*) 2
thrice = (*) 3
sixtimes = twice . thrice
```

Material: [2015-04-08_intro-to-fp-python-haskell-clojure](https://github.com/got-lambda/presentations/tree/master/2015-04-08_intro-to-fp-python-haskell-clojure)
