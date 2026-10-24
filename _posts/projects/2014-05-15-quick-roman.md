---
title: "Quick Roman"
tagline: "Got.clj meetup"
description: "What happens when you design the Roman numerals kata purely from property-based tests? Tally marks and string rewriting."
tags: [open-source, clojure, testing]
---

Quick Roman was an experiment: what happens if you design the classic Roman numerals kata purely from
property-based tests, without a single hand-picked example? I presented it at tonight's Got.clj meetup.

<!-- more -->

I started from properties rather than examples. With test.check, each one is checked against 100
randomly generated integers between 1 and 3999:

```clojure
(defspec reversible
  100
  (prop/for-all [i int-within-roman-range]
    (= (roman->decimal (decimal->roman i))
       i)))
```

There are three properties in total:

- **reversible**: converting to a Roman numeral and back gives the original number.
- **less-than-3-in-a-row**: no symbol appears more than three times in a row.
- **equivalent-addition**: adding two Roman numerals with `roman-add` gives the same result as
  adding the integers.

Nothing ever says that 14 is `"XIV"`. The properties only describe how
numerals behave, so the implementation was free to get there any way it liked.

Instead of the usual table of values and a loop, a number becomes a
string of tally marks: `decimal->roman` repeats `"I"` n times, then rewrites the string with two
tables of plain string replacements. Factorizations turn `"IIIII"` into `"V"`, `"VV"` into `"X"`,
and so on up to `"M"`; simplifications turn `"IIII"` into `"IV"`, `"VIIII"` into `"IX"`, and so on.
Going back, `roman->decimal` runs the same tables in reverse and counts the `I`s that are left.
Addition falls out almost for free: expand both numerals, concatenate, sort the symbols and simplify
again.

It's slow, it builds a string of up to 3999 `I`s, and nobody should use it. Not a good solution,
just an interesting one.

Source on GitHub: [Jell/quick-roman](https://github.com/Jell/quick-roman)

Meetup material: [2014-05-15_quickcheck-driven-development-in-clojure](https://github.com/got-lambda/presentations/tree/master/2014-05-15_quickcheck-driven-development-in-clojure)
