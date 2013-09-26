#!/usr/bin/env python

import ConfigParser
import os
import sys
import gspread

# Read config info
config = ConfigParser.ConfigParser()
config.readfp(open(os.path.expanduser('~/.gcat.conf')))

# Log in
user = config.get('User info', 'user')
password = config.get('User info', 'password')
gc = gspread.login(user, password)

# Read in spreadsheet source info
source_info = ConfigParser.ConfigParser()
source_info.readfp(sys.stdin)
sections = source_info.sections()

def removeNonAscii(s):
        return "".join(filter(lambda x: ord(x) < 128, s))

def removeNewline(s):
        return "".join(filter(lambda x: x != '\n', s))

def convertNoneToEmpty(s):
        if s:
                return s
        else:
                return ""

def cat_tables(section):
        print "=====%s" % section
        for p in source_info.items(section):
                [spreadsheet_key, worksheet_index] = p[1].split(":")
                spreadsheet = gc.open_by_key(spreadsheet_key)
                worksheet = spreadsheet.get_worksheet(int(worksheet_index))

                list_of_lists = worksheet.get_all_values()
                for row in list_of_lists:
                        row = [convertNoneToEmpty(f) for f in row]
                        conditionedLine = '\t'.join(row)
                        conditionedLine = removeNonAscii(conditionedLine)
                        conditionedLine = removeNewline(conditionedLine)
                        print "\t%s" % conditionedLine
        return

# Print out data
for s in sections:
        cat_tables(s)
