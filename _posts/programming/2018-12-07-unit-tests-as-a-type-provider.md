---
category: programming
title: "Unit Tests as a Type Provider"
tagline: "Fun code snippet"
description: "Running assertions at compile time in Idris with a type provider, so a failing test stops the build."
tags: [snippets, idris]
---

Idris type providers run an `IO` action while the module is being compiled. I used one to run a list of assertions: each passing one prints "pass", and the first failing one returns an `Error` with its description, which makes compilation fail.

```idris
module TestProvider
%default total
%access export

compileTest : List (Bool, String) -> IO (Provider String)
compileTest [] = pure $ Provide "success"
compileTest ((True, _) :: xs) = do
  printLn "pass"
  compileTest xs
compileTest ((False, description) :: xs) = do
  printLn "failed"
  pure $ Error description
```

```idris
module Test
import TestProvider
%default total
%language TypeProviders


add : Int -> Int -> Int
add x y = 0

%provide (result : String) with compileTest [
  (add 1 2 == 0, "1 + 2 = 3")
, (add 1 2 == 0, "1 + 2 = 3")
, (add 1 2 == 0, "1 + 2 = 3")
]
```

Here `add` is just a stub that returns `0`, and the assertions match it, so the module compiles.

Gist: [Test.idr, TestProvider.idr](https://gist.github.com/Jell/a1fdc65098fecfd73f15ac5027c6709b)
