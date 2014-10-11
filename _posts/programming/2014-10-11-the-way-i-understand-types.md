---
layout: post
category : programming
tagline: "The way I understand Types"
tags : [types,programming]
---

This is my (mostly wrong) way of understanding Types. I heard the best
way to get feedback on the internet is to publish something
inaccurate, so there you have it.

<!-- more -->

Types are sets of properties held by values. In a language, the more
things you have that are values, the richer your Types are.

Values can have many sorts of properties: all values that are numbers
can be added together, all values that are strings can be
concatenated, all values that are functions can be invoked.

A Type could be for instance "all values that are printable". Or even
"all values that are values". One could even devise a Type that cannot
contain any value, i.e "all values that are not values".

A Type is large if many values belong to it, and is small when few
do. The larger the Type, the smaller the sets of properties it
represents.

The largest Type a value can have is the Type of having no particular
property, also called the "Top" (⊤), or the Type of having all the
properties (⊥), which no value can belong to.

A value can have many properties: "3" is a value, a number, a
representable value, and it has the value "3".

So we could say that "3" is of Type Value, Number, Representable, and
BeingTheNumber3. We need to dispatch on those Types at some point if
we want to manipulate values.

One way to go is to keep all that information in the value itself, and
do a so-called dynamic dispatch: at runtime, simply look at the value
and see what properties it has. If it is missing the property you
need, well that's a so-called Type error.

Another way to do that is to do the dispatch statically. A program is
made of variable, that when running will hold values. They are called
variables because over time they will hold different values. A
variable has the Type of the union of the Types of all the values it
can hold at runtime.

What this means is that a variable can have the properties of all the
values it can hold, but not necessarily all at once.

We can annotate those variables before running our program (i.e
statically) with their smallest Type, or the set of property we
believe they always hold at any given time later on when we will be
running the program.

By doing so, we can use the proper implementation for a given variable
without having to look at the value itself at runtime, and we no
longer need to encode this property on the value itself.

If we have annotated a variable with a given Type, but pass on a value
with another Type, we get a Type error and unexpected behavior.

We can improve the our static dispatch approach by actually proving
that each variable will only hold values that share it's properties,
i.e is of the same Type. This requires implementing a Type checker
that can reflect on the invariances of our program and infer the Types
of each variable, and unify them with our manual annotations.

If a unification fails, we get an error. By verifying a program with a
Type checker, we can get rid of all the Type errors involving all the
Types that are expressible and used in our program.

To be noted, using dynamic dispatch does not preclude having a Type
checkers. By having proper annotations, we can still reflect on the
invariances of our program, even if that knowledge is not used at
runtime.

Not all Types are easily expressible and easy to reason about. And
proving that certain variables have a given Type can be
computationally very expensive, if possible at all.
