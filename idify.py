#!/usr/bin/env python

import hashlib
import sys

for line in sys.stdin:
    fields = line.split("\t")
    name = fields[2]
    sha1 = hashlib.sha1(name.encode('utf-8')).hexdigest()[0:5]
    print("\t".join([sha1, name]))

