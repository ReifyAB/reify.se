---
title: "Immutable Record"
tagline: "RubyGem"
description: "Immutable Ruby values inspired by Clojure's records, printed in a form you can paste back into IRB."
tags: [open-source, ruby, clojure]
---

ImmutableRecord is a small gem for immutable values in Ruby, inspired by Clojure's records. `ImmutableRecord.new(:foo, :bar)` returns a class with readers only, a constructor that rejects missing or unknown keys, and equality by value, so records work as hash keys. Instances are frozen; to change something, `clone` returns a new record.

Like Clojure's data, a record prints as code that builds it: copy what IRB shows you, paste it back in, and you get an equal value.

```ruby
Item = ImmutableRecord.new(:foo, :bar)
item = Item.new(foo:1, bar:2)
#=> Item[{:foo=>1, :bar=>2}]

item.clone(foo: "changed")
#=> Item[{:foo=>"changed", :bar=>2}]
```

It started as a [gist](https://gist.github.com/Jell/e276d8198e3191796580) last autumn.

Install it with `gem install immutable_record`, or see it on [RubyGems](https://rubygems.org/gems/immutable_record).
