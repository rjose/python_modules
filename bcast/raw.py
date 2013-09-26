#-------------------------------------------------------------------------------
# 'Parses' text from file "f" as python dictionary.
#
# This makes no assumptions about the format or structure of the data. Any
# "title" should be part of the raw text (but won't be formatted as a title).
#
def parse(f):
        title = 'Raw text'
        data = f.read()
        result = {'title': title, 'command': 'raw', 'data': data}
        return result
