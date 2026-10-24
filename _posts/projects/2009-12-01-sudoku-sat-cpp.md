---
title: "Sudoku as SAT"
tagline: "Chalmers"
description: "A small C++ program that turns a Sudoku grid into a propositional formula and hands it to the Satzoo SAT solver."
tags: [open-source, c++, sudoku]
---

A Sudoku solver I wrote at Chalmers, in C++. It doesn't search at all: it describes the puzzle and lets a SAT solver do the work. It reads a grid from `matrix.txt` and writes `sudoku.prop`, a formula over 729 variables where `sijk` means "cell (i, j) holds k". The givens become facts, every cell needs at least one digit, and if a cell holds k, no other digit is in that cell and no other cell in its row, column or box holds k. Satzoo solves it, and the program reads the model back to print the grid. Each cell's "at least one digit" constraint looks like this:

```
(s111|s112|s113|s114|s115|s116|s117|s118|s119)&
```

Source on GitHub: [Jell/sudoku-sat-cpp](https://github.com/Jell/sudoku-sat-cpp)
