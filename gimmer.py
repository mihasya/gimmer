#!/usr/bin/env python

# gimmer is a wrapper around mcollective's mc-find-hosts utility that tries to
# make it easier to find hosts by using heuristics (read: regular expressions)
# to determine which "fact" the user is in fact interested in; the goal is to
# save the user from having to remember the actual names of facts (such as
# ipaddress_eth0 - how many underscores are there? or ec2_placement) and type
# them out every time.

# the ultimate goal is to provide customizable "transforms" which will allow
# people to create their own shortcuts by placing them in a dotfile.

# gimmer's name is derrived from the word "gimme" like "gimme some fucking
# hosts." The urban dictionary page for the word was discovered after the fact,
# though it doesn't really contribute anything interesting, ironic, or funny.
# http://www.urbandictionary.com/define.php?term=gimmer

from sys import argv
from os import execv, getenv
import re

def import_patterns(filename, patterns):
    f = open(filename, 'r')
    for line in f:
        dict_line = "{%s}" % line.strip()
        patterns.update(eval(dict_line))
    return patterns

def transform(arg):
    for pattern, replacement in patterns.iteritems():
        (result, subs) = re.subn(pattern, replacement, arg)
        if (subs > 0):
            return result
    # return as is
    return arg

# TODO: make this configurable
mc_bin = "/usr/sbin/mc-find-hosts"

# mapping of patterns and their replacements
patterns = {}

filenames = ["/etc/gimmer", "%s/.gimmer" % getenv("HOME")]

for filename in filenames:
    try:
        import_patterns(filename, patterns)
    except IOError, e:
        pass

arguments = map(transform, argv[1:])

print "arguments: %s" % " ".join(arguments)

# pad the arguments since mcollective seems to swallow the first one
arguments = [''] + arguments

# hand it over to mcollective
execv(mc_bin, arguments)
