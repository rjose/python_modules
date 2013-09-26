import re

#===============================================================================
# Internal declarations
#
START = "START"
COLLECTING = "COLLECTING"

#===============================================================================
# Public API
#

#-------------------------------------------------------------------------------
# Splits text from file f into sections according to headers.
#
# The format of the text looks something like this:
#
# =====section1
#   Block of text
# =====section2
#   Block of text
#
# NOTE: Each line in the block of input text starts with a tab character.
#
# This returns a dictionary of header labels (like section1) to string (the
# contents of the stream).
#
def sectionize(f):
    state = {
        'result': {},
        'state': START,
        'cur_section': ''
    }

    for line in f.readlines():
        handle_line(state, line)

    # Strip trailing '\n' from each section
    for k, v in state['result'].items():
        state['result'][k] = v.rstrip()

    return state['result']


#===============================================================================
# Internal functions
#

#-------------------------------------------------------------------------------
# Helper function for splitting text into sections.
#
def handle_line(state, line):
    cur_section = state['cur_section']

    # If the state is START, then we're looking for a section heading. This has
    # the format "=====title". If we can't find such a heading, bail out.
    if state['state'] == START:
        m = re.match("=====(.+)", line)
        if (not m):
            raise Exception("Couldn't find separator. Got %s" % line)
        state['state'] = COLLECTING
        cur_section = m.group(1)
        state['cur_section'] = cur_section
        state['result'][cur_section] = ""

    # If the state is COLLECTING, then we're putting all of the lines into the
    # cur_section of the result. We expect the first character of each line
    # that we're collecting to be '\t'.
    elif state['state'] == COLLECTING:
        if line[0] == '=':
            state['state'] = START
            handle_line(state, line)
        elif line[0] != '\t':
            raise Exception("Text in sections must start with a tab char")
        else:
            state['result'][cur_section] += line[1:]
    else:
        raise Exception("Unknown state: %s" % state['state'])
    return
