---
category: programming
title: "FizzBuzz with Qualified Constants"
tagline: "Fun code snippet"
description: "FizzBuzz without arithmetic: nested Ruby modules and constant lookup do the modulo for you."
tags: [snippets, ruby]
---

A FizzBuzz with no modulo operator. Instead, I nest three `T` modules and five `F` modules, mark the innermost one with a `zero` method, and look up `T::T::...::T` with `n` segments.

```ruby
require 'active_support/core_ext'

module T
  module T
    module T
      def self.zero; end
    end
  end
end

module F
  module F
    module F
      module F
        module F
          def self.zero; end
        end
      end
    end
  end
end

def fizz_buzz (n)
  mod3 = Object.qualified_const_get((["T"]*n).join("::"))
  mod5 = Object.qualified_const_get((["F"]*n).join("::"))
  if mod3.respond_to?(:zero) && mod5.respond_to?(:zero)
    "FizzBuzz"
  elsif mod3.respond_to?(:zero)
    "Fizz"
  elsif mod5.respond_to?(:zero)
    "Buzz"
  else
    n
  end
end

(1..20).map(&method(:fizz_buzz))
#=> [1, 2, "Fizz", 4, "Buzz", "Fizz", 7, 8, "Fizz", "Buzz", 11, "Fizz", 13, 14, "FizzBuzz", 16, 17, "Fizz", 19, "Buzz"]
```

When a lookup goes past the innermost module, Ruby's constant resolution falls back to the top-level `T` (or `F`), so the chain wraps around and the module reached only responds to `zero` when `n` is a multiple of 3 (or 5).

Gist: [fizzbuzz_constants.rb](https://gist.github.com/Jell/d94f73f97b2968e8c496)
