---
title: "Advent of Code in SQL"
description: "Seventeen days of Advent of Code 2020, each solved with a single query in pure PostgreSQL."
tags: [open-source, sql, advent-of-code]
---

For Advent of Code 2020 I set myself one rule: pure SQL, as standard as possible, with no custom
functions, and a single PostgreSQL query per puzzle. It got me through 17 days. Thanks to Vik
Fearing, whose own Postgres solutions got me started.

Some of the techniques that made it possible:

- **Recursive CTEs** for anything loop-shaped: walking a graph of bags, running a small program
  interpreter, a stack-based calculator, even Conway's Game of Life in 3D.
- **Lateral joins** to parse each line of input and feed one step into the next.
- **Regular expressions** to split and match the input, and once to build a regex out of the
  puzzle's own grammar.
- **Window functions** for numbering and ordering things.
- **Arrays** as stacks and as lists of what's already been visited.
- **Bit strings** for the binary puzzles: boarding passes become `bit(7)`, and bitmasks are
  applied with `bit(36)`.

Source on GitHub: [Jell/advent2020](https://github.com/Jell/advent2020)
