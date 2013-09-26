#!/usr/bin/env python

import sys
import datetime

# NOTE: These aren't strictly correct, but they're good enough for planning
quarter_dates = {}
quarter_dates['Q1'] = ["Jan 1", "Mar 31"]
quarter_dates['Q2'] = ["Apr 1", "Jun 30"]
quarter_dates['Q3'] = ["Jul 1", "Sep 30"]
quarter_dates['Q4'] = ["Oct 1", "Dec 31"]

now = datetime.datetime.now()
year = now.year
start = None
end = None

# Bail out if not enough info
if len(sys.argv) == 1:
        sys.stderr.write("Usage: weeks_left.py Q1 [2013]")
        sys.exit(-1)

quarter = sys.argv[1]
if len(sys.argv) >= 3:
        year = sys.argv[2]

[start, end] = [datetime.datetime.strptime("%s, %s" % (d, year), "%b %d, %Y")
                for d in quarter_dates[quarter]]

if now > start:
        start = now

if now > end:
        end = now

delta = (end - start).days/7.0
print("%.1f" % delta)
