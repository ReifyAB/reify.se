---
layout: post
category : programming
tagline: "fun with code inference"
tags : [types,programming]
---

Idris is a one of those programming languages that empowers its users
with the possibility to express very strong guarantees about the code
they write before running it. It does this by using something called
"Dependent Typing", which is a very expressive kind of type system.

One of the guarantees you can get is to have safe arithmetic with
natural numbers (0, 1, 2, 3...). The interesting bit with Natural
numbers is that they cannot be negative, so the substraction `a - b`
only works if `a > b`. Idris actually forces you to make sure of that
before trying to run your code.

<!-- more -->

# Playing around with Nat

Let's look at some code:

```idris
foo : Nat
foo = 4 - 3
```

Idris will gladly compile, then you can ask the value of `foo` at the REPL to evaluate the result:

```
λΠ> foo
1 : Nat
```

Now if we try another case where `a` is smaller than `b`, then idris will not be happy:

```idris
foo : Nat
foo = 2 - 3

- + Errors (1)
 `-- fun.idr line 17 col 8:
     When checking right hand side of foo with expected type
             Nat

     When checking argument smaller to function Prelude.Nat.-:
             Can't find a value of type
                     LTE 3 2
```

So it fails to compile, and tells you it cannot prove that 3 is
smaller than 2.

That's pretty neat! Now how smart is idris then? Let's try!

```idris
foo : Nat
foo = (2 + 2) - 3
```

Yup! That works! Neat, so Idris can figure out that `2 + 2 > 3` at
compile time. Let's try something harder: can we abstract over one of
the parameters?

```idris
foo : Nat -> Nat
foo n = n - 3

- + Errors (1)
 `-- fun.idr line 17 col 10:
     When checking right hand side of foo with expected type
             Nat

     When checking argument smaller to function Prelude.Nat.-:
             Can't find a value of type
                     LTE 3 n
```

Ok so that makes sense: Idris is not happy because it cannot prove
that given any natural number `n`, `n` is smaller than `3`. (for
instance, if `n = 2` then that's not true).

But wait...

```idris
foo : Nat -> Nat
foo n = (3 + n) - 3
```

OMG! Yep that compiles! So Idris manages to figure out that given any
natural number `n`, `3 + n > 3`! That's really cool!

It does that just by itself, without me having to prove anything.

# How does that work?

Let's look a bit closer at the `-` function:


```idris
λΠ> :doc (-)
Prelude.Nat.(-) : (m : Nat) -> (n : Nat) -> {auto smaller : LTE n m} -> Nat

    infixl 8

    The function is Total
```

The first line is the type of the function, and wow, it's a bit more
complicated than I expected... Let's look at it closer:

`(m : Nat)` and `(n : Nat)` are the two arguments to the functions, so
we can read `(m : Nat) -> (n : Nat) -> ...` as "given any natural number `m` and any natural number
`n`, ...".

The next part is this big thingy: `{auto smaller : LTE n m}`. Let's
unpack this a bit.

The curly braces `{}` in the type means it's an implicit parameter:
it's not passed explicitely, and should be derivable from
context. `auto` is a keyword that tells Idris to automatically derive
that parameter from context. So if we removed all that fluff, we could
rewrite the type like this:

```idris
Prelude.Nat.(-) : (m : Nat) -> (n : Nat) -> (smaller : LTE n m) -> Nat
```

Which would read like:

Given a natural number `m`, a natural number `n`, and a proof
"`smaller`" that `n` is less than `m`, you'll get a natural number
out.

The magic happens when adding the curly-braces and the `auto` keyword,
as this proof can be found by Idris automatically.

OK maybe that's a bit too much... Perhaps the best way is to try to re-implement all of that ourselves from scratch.

# Let's build numbers from scratch

Let's first define natural numbers. We can define them recursively, by
saying it's either `0` or the successor of another natural number:

```idris
data MyNat : Type where
  MZ : MyNat
  MS : MyNat -> MyNat
```

So `0` is `MZ`, `1` is `MS MZ`, `2` is `MS (MS MZ)`... That's actually
how natural numbers are implemented in idris (using the digits
representation is just sugar).

So we can implement addition like this. First we declare the type of addition:

```idris
mplus : MyNat -> MyNat -> MyNat
```

It says "given a natural number and another natural number I'll give
you another natural number". From that and from your text editor, you
can ask Idris to add a placeholder body for the function definition
(in emacs, `C-c C-s`)

```idris
mplus : MyNat -> MyNat -> MyNat
mplus x y = ?mplus_rhs
```

The part with a question mark is what needs to be filled. If you evaluate that code in idris (`C-c C-l`), Idris will tell you something like this:

```idris
Holes

This buffer displays the unsolved holes from the currently-loaded code. Press
the [P] buttons to solve the holes interactively in the prover.

- + Main.mplus_rhs [P]
 `--               x : MyNat
                   y : MyNat
     ------------------------
      Main.mplus_rhs : MyNat
```

What this says is that there is a "hole" (`mplus_rhs`) in your program
of type `MyNat`, and that to fill that hole you have 2 parameters at
your disposition (`x` and `y`) with a similar type. But this doesn't
allow us to define addition, so we can ask Idris to do a case split on
the first argument to see if we can get more things at our disposal.

In emacs you do that by putting your cursor on the first argument and
pressing `C-c C-c`, resulting in this:

```idris
mplus : MyNat -> MyNat -> MyNat
mplus MZ y = ?mplus_rhs_1
mplus (MS x) y = ?mplus_rhs_2
```

Which after you load (`C-c C-l`) you get:

```idris
Holes

This buffer displays the unsolved holes from the currently-loaded code. Press
the [P] buttons to solve the holes interactively in the prover.

- + Main.mplus_rhs_1 [P]
 `--                 y : MyNat
     --------------------------
      Main.mplus_rhs_1 : MyNat

- + Main.mplus_rhs_2 [P]
 `--                 x : MyNat
                     y : MyNat
     --------------------------
      Main.mplus_rhs_2 : MyNat
```

If we look at the first case, the first argument is zero. In that case
we just need to return the second argument (`0 + y = y`). Since nothing is ambiguous here, we can even ask idris to fill that for us by putting the cursor on `?mplus_rhs_1` and performing a "proof search" (pressing `C-c C-a`):

```idris
mplus : MyNat -> MyNat -> MyNat
mplus MZ y = y
mplus (MS x) y = ?mplus_rhs_2
```

This went like this: when performing the proof search, Idris looked at
the type of the hole, and whatever was available from context that
matched that type (in this case, only `y` was available), and used
that to fill the hole!

Pretty neat eh?

Now the second bit if we do the same we get the same result:

```idris
mplus : MyNat -> MyNat -> MyNat
mplus MZ y = y
mplus (MS x) y = y
```

Obviously Idris cannot read our mind. If we ask Idris to fill a hole
with a given type, it just provides the simple possible answer for
that, in this case `y`.

Fine, let's just use our human brains. We can use the property that `(1 + x) + y = 1 + (x + y)`:


```idris
mplus : MyNat -> MyNat -> MyNat
mplus MZ y = y
mplus (MS x) y = MS (mplus x y)
```

We can try it out at the REPL:

```idris
λΠ> mplus (MS (MS MZ)) (MS (MS MZ))
MS (MS (MS (MS MZ))) : MyNat

λΠ> mplus (MS (MS MZ)) MZ
MS (MS MZ) : MyNat
```

OK it hurts the eye a little but we can see that `2 + 2 = 4` and `2 +
0 = 2`.

Now let's move to substraction. First the type:

```idris
mminus : MyNat -> MyNat -> MyNat
```

Then add the body automatically:

```idris
mminus : MyNat -> MyNat -> MyNat
mminus x y = ?mminus_rhs
```

Case split on the second argument:

```idris
mminus : MyNat -> MyNat -> MyNat
mminus x MZ = ?mminus_rhs_1
mminus x (MS y) = ?mminus_rhs_2
```

OK `x - 0 = x` so we can fill the first case:

```idris
mminus : MyNat -> MyNat -> MyNat
mminus x MZ = x
mminus x (MS y) = ?mminus_rhs_2
```

For the second case we need to split again on `x` actually:

```idris
mminus : MyNat -> MyNat -> MyNat
mminus x MZ = x
mminus MZ (MS y) = ?mminus_rhs_1
mminus (MS x) (MS y) = ?mminus_rhs_3
```

OK last case we can use the fact that `(x + 1) - (y + 1) = x - y`:

```idris
mminus : MyNat -> MyNat -> MyNat
mminus x MZ = x
mminus MZ (MS y) = ?mminus_rhs_1
mminus (MS x) (MS y) = mminus x y
```

But the middle case is actually annoying: what is the answer to `0 -
x` for natural numbers? That's annoying because natural numbers do not
contain negative numbers!

So we need to somehow constrain the input in such a way that this case
is impossible, i.e. we need to have a proposition that given `x` and
`y`, `y` is smaller than `x`.

# Building math from scratch

How do we do that? Actually similarly to how we defined natural numbers:

 - Any natural number is larger than zero
 - If `n < m`, then `(n + 1) < (m + 1)`

In Idris that translates to something like this:

```idris
data MyLTE  : (m : MyNat) -> (n : MyNat) -> Type where
  MyLTEZero : MyLTE MZ right
  MyLTESucc : MyLTE left right -> MyLTE (MS left) (MS right)
```

So if you want to write `0 < 2`, you would write:

```idris
MyLTEZero MZ (MS (MS MZ))
```

If you want to write `2 < 3`, you would write:

```idris
(MyLTESucc (MyLTESucc (MyLTEZero MZ (MS MZ))))
```

Really the above is a way to construct a proof that `2 < 3` more than
a way to ask the question "is `2` less than `3`?". This is a fact
derived from the definitions we've given for "what is a natural
number?" and "what does it mean for a natural number to be less than
or equal to another natural number?"

Anywho, let's start over our definition of minus, this time requiring
a proof that `m < n`:

```idris
mminus : (m : MyNat) -> (n : MyNat) -> MyLTE n m -> MyNat
```

Add body:

```idris
mminus : (m : MyNat) -> (n : MyNat) -> MyLTE n m -> MyNat
mminus m n x = ?mminus'_rhs
```

This time we split on the proof (`x`):

```idris
mminus : (m : MyNat) -> (n : MyNat) -> MyLTE n m -> MyNat
mminus m MZ MyLTEZero = ?mminus'_rhs_1
mminus (MS right) (MS left) (MyLTESucc x) = ?mminus'_rhs_2
```

Cool! This is where the "dependent type" magic happens: case splitting
on the proof has an effect on the arguments `m` and `n`: if the proof
you provide is `0 < m`, then clearly `n = 0`, and if the proof you
provide looks like `(1 + x) < (1 + y)`, then clearly `m` and `n` are
not zero.

So let's fill in some of the logic:

```idris
mminus : (m : MyNat) -> (n : MyNat) -> MyLTE n m -> MyNat
mminus m MZ MyLTEZero = m
mminus (MS right) (MS left) (MyLTESucc x) = mminus right left ?prf
```

If we look at the hole left for the proof in the recursive part of this function, we see this:

```idris
- + Main.prf [P]
 `--     right : MyNat
          left : MyNat
             x : MyLTE left right
     -----------------------------
      Main.prf : MyLTE left right
```

There's a hole of type `MyLTE left right` and a parameter `x` of type `MyLTE left right`! Cool, perhaps we can just ask Idris to fill that up for us! (`C-c C-a`)

```idris
mminus : (m : MyNat) -> (n : MyNat) -> MyLTE n m -> MyNat
mminus m MZ MyLTEZero = m
mminus (MS right) (MS left) (MyLTESucc x) = mminus right left x
```

Neat!! Now let's try to use that method a bit:

```idris
foo : MyNat
foo = mminus (MS (MS (MS MZ))) (MS MZ) ?prf
```

This is `3 - 1` with a hole for the proof.

The hole looks like this:

```idris
- + Main.prf [P]
 `-- MyLTE (MS MZ) (MS (MS (MS MZ)))
```

OK... So how do we proceed? Let's just ask Idris to see if it can figure out something (`C-c C-a`):

```idris
foo : MyNat
foo = mminus (MS (MS (MS MZ))) (MS MZ) (MyLTESucc MyLTEZero)
```

AAAH! That worked! How is that possible? Actually Idris can try to
find proof by looking a the constructors available for the type of the
hole (in our case, `MyLTEZero` and `MyLTESucc x`) and try to build a
value using those constructors.

Neat!

# Hide the math!

So can we make that process automatic then? Yes if we introduce
the proof as an implicit parameter and add the `auto` keyword! Let's try:

```idris
mminus : (m : MyNat) -> (n : MyNat) -> {auto smaller : MyLTE n m} -> MyNat
```

Add the body:

```idris
mminus : (m : MyNat) -> (n : MyNat) -> {auto smaller : MyLTE n m} -> MyNat
mminus m n = ?mminus_rhs
```

Wait... Where's the proof in the body? OK actually with implict
parameters, you have to explicitely say you need them:

```idris
mminus : (m : MyNat) -> (n : MyNat) -> {auto smaller : MyLTE n m} -> MyNat
mminus {smaller} m n = ?mminus_rhs
```

Case split on the proof:

```idris
mminus : (m : MyNat) -> (n : MyNat) -> {auto smaller : MyLTE n m} -> MyNat
mminus {smaller = MyLTEZero} m MZ = ?mminus_rhs_1
mminus {smaller = (MyLTESucc x)} (MS right) (MS left) = ?mminus_rhs_2
```

And fill the rest:

```idris
mminus : (m : MyNat) -> (n : MyNat) -> {auto smaller : MyLTE n m} -> MyNat
mminus {smaller = MyLTEZero} m MZ = m
mminus {smaller = (MyLTESucc x)} (MS right) (MS left) = mminus right left
```

And now we can try again our substraction:

```idris
foo : MyNat
foo = mminus (MS (MS (MS MZ))) (MS MZ)
```

Sweet! And if we do something more funky:

```idris
foo' : MyNat -> MyNat
foo' n = mminus (mplus (MS MZ) n) (MS MZ)
```

Yep that still works! Neato. Wait so how about this:

```idris
foo'' : MyNat -> MyNat
foo'' n = mminus (mplus n (MS MZ)) (MS MZ)

- + Errors (1)
 `-- fun.idr line 48 col 17:
     When checking right hand side of foo'' with expected type
             MyNat

     When checking argument smaller to function Main.mminus:
             Can't find a value of type
                     MyLTE (MS MZ) (mplus n (MS MZ))
```

Ah noes! That didn't work... The reason for that is that Idris has no
idea that `3 + n = n + 3`, and we've defined addition by case
splitting on the first argument...

Well, that's for another time!

# Conclusion

I hope this gave you some idea of how powerful and the kind of
guarantees that can be expressed in Idris and gave some insights on
how things can be made practical (not having to provide or carry
proofs when those proofs can be derived from context).
