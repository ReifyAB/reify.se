---
layout: post
category : programming
tagline: "aka flamebaiting"
tags : [types,programming]
---

This is my (mostly wrong) way of understanding types. I heard the best
way to get feedback on the internet is to publish something
inaccurate, so there you have it.

<!-- more -->

Types are sets of properties held by values. In a language, the more
things you have that are values, the richer your types are.

Values can have many sorts of properties: all values that are numbers
can be added together, all values that are strings can be
concatenated, all values that are functions can be invoked.

A type could be for instance "all values that are printable". Or even
"all values that are values". One could even devise a type that cannot
contain any value, i.e "all values that are not values".

A type is large if many values belong to it, and is small when few
do. The larger the type, the smaller the sets of properties it
represents.

The largest type a value can have is the type of having no particular
property, so all values belong to it, whereas the smallest type is the
type of having all the imaginable properties at once, which is
impossible so no value can belong to it.

A value can have many properties: "3" is a value, a number, a
representable value, and it has the value "3".

So we could say that "3" is of type Value, Number, Representable, and
BeingTheNumber3. We need to dispatch on those types at some point if
we want to manipulate values.

One way to go is to keep all that information in the value itself, and
do a so-called dynamic dispatch: at runtime, simply look at the value
and see what properties it has. If it is missing the property you
need, well that's a so-called type error.

Another way to do that is to do the dispatch statically. A program is
made of variables that when running will hold values. They are called
variables because over time they will hold different values. A
variable has the type of the union of the types of all the values it
can hold at runtime.

What this means is that a variable can have the properties of all the
values it can hold, but not necessarily all at once.

We can annotate those variables before running our program (i.e
statically) with their smallest type, that is the set of property we
believe they will always hold at any given time later on when we
actually run the program.

By doing so, we can use the proper implementation for a given variable
without having to look at the value it is holding at runtime, so we no
longer need to encode this property on the value itself.

If we have annotated a variable with a given type, but pass on a value
with another type, we get a type error and unexpected behavior.

We can improve our static dispatch approach by actually proving that
each variable will only hold values that share its properties, i.e are
of the same type. This requires implementing a type checker that can
reflect on the invariances of our program and infer the types of each
variable without running it.

If a unification fails, we get an error. By verifying a program with a
type checker, we can get rid of all the type errors involving all the
types that are expressible and used in our program.

To be noted, using dynamic dispatch does not preclude having a type
checkers. By having proper annotations, we can still reflect on the
invariances of our program, even if that knowledge is not used at
runtime.

Not all types are easily expressible and easy to reason about. And
proving that certain variables have a given type can be
computationally very expensive, if possible at all. But the more is
expressed in the type system, the less can go wrong at runtime.
