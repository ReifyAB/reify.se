---
category: engineering
title: "SSH port-forwarding using a socket file"
tagline: "Treyd tech blog"
description: "Forward a remote Postgres through a bastion to a local socket file, so psql never fights over port 5432."
tags: [ssh, postgresql, bash, platform-engineering]
---
I came across this neat trick when trying to set up access to a database running in a private network.

The context is that I wanted to write a small bash script that would set up port-forwarding through a bastion instance to allow me to connect to that database from my local machine.

<!-- more -->

What I started with was to first start a tunnel in one terminal:

```bash
ssh $BASTION_HOSTNAME -4 -N -L 5432:$DATABASE_HOST:5432
```

Then connect to it using `psql` in another:

```
psql --host=localhost --port=5432 --dbname=my-database
```

Let's unpack those SSH flags real quick:

* `-4`: use IPv4 (not strictly necessary, but I've had issues without it sometimes when trying to connect using IPv6)
* `-N`: do not forward any command, good when you just want to do port forwarding as in our case
* `-L <LOCAL_PORT>:<REMOTE_ADDRESS>:<REMOTE_PORT>`: forward packets from `localhost:<LOCAL_PORT>` to `<REMOTE_ADDRESS>:<REMOTE_PORT>`

The annoying thing though is that if I already have a local database running on port `5432`, I get an error:

```
bind [127.0.0.1]:5432: Address already in use
channel_setup_fwd_listener_tcpip: cannot listen to port: 5432
Could not request local forwarding.
```

If I want to make it work I would have to find a free port, then use that port for setting up the SSH tunnel and the psql connection.

But looking at the man page for SSH, I found the following:

```
     -L [bind_address:]port:host:hostport
     -L [bind_address:]port:remote_socket
     -L local_socket:host:hostport
     -L local_socket:remote_socket
```

Turns out, `ssh` can also forward from & to socket files? Interesting...

And then I ran the documentation for psql using `man psql` and found:

```
       -h hostname
       --host=hostname
           Specifies the host name of the machine on which the server is running. If the value begins with a slash, it is used as the directory for
           the Unix-domain socket.
```

If the hostname starts with a slash, it will connect using a socket file!

Then I could set up SSH port forwarding to a local socket file, then connect to the instance using psql through that socket file!

That means I can also do that many times in parallel without worrying about conflicting ports, meaning I could write a small script that:
1. creates a socket file
2. sets up SSH port forwarding to the database through that socket file
3. start psql by connecting to the same socket file

This does the trick:

```bash
#!/usr/bin/env bash

set -euo pipefail

POSTGRES_SOCKET_FOLDER=$(mktemp -d -t postgres-XXXXXX)
POSTGRES_SOCKET=$POSTGRES_SOCKET_FOLDER/.s.PGSQL.5432

ssh $BASTION_HOSTNAME -f -4 -N -L $POSTGRES_SOCKET:$DATABASE_HOST:5432

psql --host=$POSTGRES_SOCKET_FOLDER --dbname=my-database
```

The only thing I also need to figure out is out to close the SSH tunnel and clean up the socket file once I quit psql. That's something we can do with a `trap EXIT` and `pkill`:

```bash
function cleanup {
  echo -n "Stopping bastion connection..."
  pkill -f $POSTGRES_SOCKET
  rm -r $POSTGRES_SOCKET_FOLDER
  echo "done."
}

trap "cleanup" EXIT
```

Neato! Here is the full script, you would have to provide `$BASTION_HOSTNAME`, `$DATABASE_HOST`, `PGUSER`, and `PGPASSWORD` as environment variables if you want to make it work in your setup:

```bash
#!/usr/bin/env bash

set -euo pipefail

POSTGRES_SOCKET_FOLDER=$(mktemp -d -t postgres-XXXXXX)
POSTGRES_SOCKET=$POSTGRES_SOCKET_FOLDER/.s.PGSQL.5432

function cleanup {
  echo -n "Stopping bastion connection..."
  pkill -f $POSTGRES_SOCKET
  rm -r $POSTGRES_SOCKET_FOLDER
  echo "done."
}

trap "cleanup" EXIT

ssh $BASTION_HOSTNAME -f -4 -N -L $POSTGRES_SOCKET:$DATABASE_HOST:5432

psql --host=$POSTGRES_SOCKET_FOLDER --dbname=my-database
```
