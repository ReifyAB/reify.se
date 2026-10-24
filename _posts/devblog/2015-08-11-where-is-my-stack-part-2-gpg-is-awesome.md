---
category: engineering
title: "Where is my stack? (Part 2): GPG is awesome"
tagline: "PugglePay dev blog"
description: "Sharing secrets with GPG instead of a shared password, and the small Ruby library we wrote for it."
tags: [gpg, security, ruby]
---
Storing and sharing secrets is tricky. At PugglePay we used to do it
by having a password encrypted file, and sharing that password with
all the devs.

This actually became a problem as we grew, because sharing a password
is annoying. If we need to change the password for safety reasons, we
need to communicate that to all devs.

The solution is of course to use GPG encryption, and it's actually not
that difficult either.

<!-- more -->

## What is GPG?

GPG is a GNU implementation of the OpenPGP standard, a set of tools
for encrypting and signing messages.

PGP encryption works by encrypting the message you want to protect
using a symetric key, then encrypting that key for each recipient of
the message using asymetric encryption.

The result of that is that each recipient has a set of public and
private keys. You only need their public key to encrypt a message, but
they will need their private key do decrypt it.

## How to create a key pair?

First install a gpg package. On mac using brew, that would be:

```
brew install gpg
```

After that, use the `--gen-key` function:

```
gpg --gen-key
```

Follow the instructions, using whatever email you want to use as your
key ID, then export the public key:

```
gpg --export -a [email] > public.key
```

You can now use that public key (or a list of them) to encrypt a file
using `gpg --encrypt`.

## How to use it to share secrets?

That's actually pretty easy: just encrypt a file containing all the
secrets using the public key of all your devs in a format that is
easily parsable in your language of choice.

We wrote a small library to do that in ruby: <https://github.com/Zimpler/mrf>

## How to edit a GPG file?

You have several options. The easy one is to use an editor that
supports editing GPG files. If you use emacs, you're lucky because
that's built-in. If you use VIM, you can use a plugin.

Alternativelly, you can use <https://gpgtools.org/>, which you might
want to install anyway because that's a good set of tools.

Worst case, use `gpg --decrypt`, change the secrets, then re-encrypt
using `gpg --encrypt`.

## Conclusion

GPG is awesome, and we've also been using it to share one-off secrets
we want to communicate over an insecure channel (like in a slack forum
or in an email).
