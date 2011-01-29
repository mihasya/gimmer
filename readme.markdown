### WTF?

I'm sure this kind of script has been written a million times. I had a need for
it (mc-find-hosts was wearing on my will to live), so I wrote another one.

It's a translator for command line arguments. You can configure it to transform
anything into anything, as long as you know the Python regular expressions
syntax.

### Configuration

gimmer looks in /etc/gimmer and ~/.gimmer for files to import patterns from. It
evals every line in the file, assuming that it will result in a dictionary if
{}'s are added to the ends. It then runs every command line argument through
the list of patterns until one applies. If none apply, it passes the argument
along as is.

#### Environment Variables

* `GIMMER_BINARY` determines what binary the script execs

It runs execv on the binary it's configured to use with the resulting list of
arguments.

### Example: mc-find-hosts

The default binary is `mc-find-hosts`, because that's what I fucking needed it
for. It can be overriden (see **Environemnt Varibles**).

Some sample patterns are found in `.gimmer.sample` For example,

`"^(i\-\w+)$": "-Fec2_instance_id=\g<1>"`

will recognize any argument that looks like an instance ID (i-23adf34) and turn
it into `-Fec2_instance_id=i23adf34` and the resulting mc-find-hosts command
will find that instance.

