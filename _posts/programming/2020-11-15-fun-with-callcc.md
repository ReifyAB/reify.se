---
category: programming
title: "Fun with callcc"
tagline: "Fun code snippet"
description: "Autovivifying nested hashes in Ruby by monkey-patching Hash and nil with callcc, so a deep assignment travels back in time."
tags: [snippets, ruby]
---

In Ruby, `foo["bar"]["baz"]["foo"] = 1` on an empty hash blows up on `nil`. Here I patch `Hash#[]`, `nil.[]` and `nil.[]=` with `callcc` so that the final assignment builds the missing hashes after the fact.

```ruby
require "continuation"

class Hash
  alias_method :_original_lookup, :[]

  def [](key)
    _original_lookup(key).tap do
      callcc { |cc| $hash_cc = [cc]; nil }&.tap do |value_from_future|
        self[key] = value_from_future
        $hash_cc.pop.call(self)
      end
    end
  end
end

def nil.[](key)
  callcc { |cc| $hash_cc << cc; nil }&.tap do |value|
    $hash_cc.pop.call(key => value)
  end
end

def nil.[]=(key, value)
  callcc { |cc|
    $hash_cc.unshift(cc)
    $hash_cc.pop.call(key => value)
  }
end

foo = {}
foo["bar"]["baz"]["foo"] = 1

puts foo
```

Each lookup that comes up empty saves a continuation and returns `nil`. When `nil.[]=` finally runs, it jumps back into those saved lookups one by one, handing each a freshly built hash, until the original `Hash#[]` stores the result and resumes after the assignment. It prints `{"bar"=>{"baz"=>{"foo"=>1}}}`.

Gist: [timetravel.rb](https://gist.github.com/Jell/6628b51914ec890350f3128d47621468)
