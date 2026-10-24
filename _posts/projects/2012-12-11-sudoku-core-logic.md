---
title: "Sudoku with core.logic"
tagline: "Got.clj meetup"
description: "A Sudoku solver with no search algorithm, only constraints."
tags: [open-source, clojure, got-clj]
---

A small Sudoku solver in Clojure, written with core.logic for tonight's Got.clj meetup. There is no search algorithm in it: I create 81 logic variables, give each one the domain 1 to 9, unify them with the puzzle (empty cells, written as zeros, become fresh variables), and require every row, column and 3×3 square to be distinct. core.logic does the rest. It comes with a "super hard" puzzle to try it on.

```clojure
(run 1 [q]
  (everyg #(infd % sudoku-domain) cells)
  (== cells constraints)
  (== q rows)
  (everyg distinctfd rows)
  (everyg distinctfd columns)
  (everyg distinctfd squares))
```

Source on GitHub: [sudoku-core-logic](https://github.com/got-lambda/sudoku-core-logic)
