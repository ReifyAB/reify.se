---
category: programming
title: "Typing Applicative in core.typed"
tagline: "Fun code snippet"
description: "An attempt at annotating an Applicative protocol in Clojure's core.typed, using dotted type variables for a variadic fapply."
tags: [snippets, clojure]
---

I was trying to give an `Applicative` protocol type annotations with core.typed. The tricky part is `fapply*`, which takes a wrapped function of any arity plus one wrapped argument per parameter.

```clojure
(t/defprotocol Applicative
  (pure* [f-val val])
  (fapply* [f-fun f-vals]))

(t/ann-protocol [domain]
  Applicative
  pure* [(Applicative domain) domain -> (Applicative domain)]
  fapply* (t/All [x ...]
            [(Applicative [x ... x -> domain])
             (Applicative x) ... (Applicative x)
             -> (Applicative domain)]))
```

The `t/All [x ...]` binder introduces a dotted type variable, so the function type `[x ... x -> domain]` and the trailing `(Applicative x) ... (Applicative x)` arguments have to line up in number.

Gist: [applicative.clj](https://gist.github.com/Jell/8457b121c7aadbfb608d)
