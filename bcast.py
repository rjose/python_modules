#!/usr/bin/env python3.3

import argparse
import http.client
import sys
import json

# Read commandline arguments
parser = argparse.ArgumentParser(description='Broadcasts data via server')
parser.add_argument('--type')
args = parser.parse_args()

# Format data as JSON
if args.type == 'piechart':
    import bcast.piechart
    result = bcast.piechart.parse(sys.stdin)
elif args.type == 'raw':
    import bcast.raw
    result = bcast.raw.parse(sys.stdin)
elif args.type == 'shortagechart':
    import bcast.shortagechart
    result = bcast.shortagechart.parse(sys.stdin)
elif args.type == 'quadchart':
    import bcast.quadchart
    result = bcast.quadchart.parse(sys.stdin)
elif args.type == 'releasechart':
    import bcast.releasechart
    result = bcast.releasechart.parse(sys.stdin)
else:
    sys.stderr.write('Unknown type: %s\n' % args.type)
    sys.exit(1)


# Post data for broadcast
# TODO: Read host/port from config file
h = http.client.HTTPConnection('localhost:8888')
h.request("POST","/broadcast", json.dumps(result), {"Content-type": "application/json"})
