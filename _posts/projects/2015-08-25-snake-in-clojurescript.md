---
title: "Snake in ClojureScript"
tagline: "Got.clj meetup"
description: "The classic snake game in a single ClojureScript file, with Reagent for rendering and a pure function for each game step."
tags: [open-source, clojurescript]
---

Snake in ClojureScript is the classic snake game, written with ClojureScript and Reagent at tonight's Got.clj meetup. The whole thing fits in a single file, `src/snake/core.cljs`.

<!-- more -->

The game state is one plain map in a Reagent atom: the frame count, the score, the apple's position, a dead flag and the snake itself, which is a direction plus a list of body coordinates.

Each step of the game is a pure function from state to state. `tick` just threads the state through the steps:

```clojure
(defn tick [state]
  (-> state
      (update :frame inc)
      move?
      eat?
      dead?))
```

`move?` pushes a new head onto the body and drops the tail unless the snake is growing, `eat?` checks for the apple and bumps the score, and `dead?` checks for hitting a wall or the snake's own tail.

The game loop is a `setTimeout` that calls `swap! app-state tick` five times a second. The arrow keys only change the snake's direction in the atom.

Rendering is a single Reagent component that draws the board as a 19 by 19 HTML table, with Figwheel for live reloading and Devcards for poking at the state.

Source on GitHub: [Jell/snake-clojurescript](https://github.com/Jell/snake-clojurescript)
