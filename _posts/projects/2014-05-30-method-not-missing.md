---
title: "Method not missing"
tagline: "RubyGem"
description: "A Ruby gem that implements your missing methods for you, by googling them."
tags: [open-source, ruby]
---

Why write methods when someone on the internet has already written them? With method_not_missing,
calling a method that doesn't exist googles `"def your_method"` on rubydoc.info, evals the first
implementation it finds into your object, and runs it.

<!-- more -->

```ruby
require "method_not_missing"

object = MethodNotMissing::OmnipotentObject.new
object.update([3])
## Googling...
#=> [3]
object.update([4])
#=> [3, 4]
```

If a candidate raises an error, it simply tries the next search result. Missing classes are made up
on the spot. On the roadmap: type safety, and "Enterprise".

Source on GitHub: [Jell/method_not_missing](https://github.com/Jell/method_not_missing)
